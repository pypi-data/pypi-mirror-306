import asyncio
import time
import base64
import json
import requests
from requests.auth import HTTPBasicAuth
from asn1crypto import x509
from encrypt import decrypt_data

from AuroraSign.aurora_signature.sign import signers, fields, timestamps
from AuroraSign.aurora_signature.sign.signers.pdf_signer import PdfTBSDocument, DSSContentSettings
from AuroraSign.aurora_signature.pdf_utils.incremental_writer import IncrementalPdfFileWriter

from AuroraSign.aurora_certvalidator import ValidationContext
from AuroraSign.aurora_certvalidator.registry import SimpleCertificateStore

from AuroraSign.aurora_signature.pdf_utils.format import format_date

BYTES_RESERVED = 30842 #20560
PPLG_DOMAIN_URL = 'http://127.0.0.1:5000'

def pplg_request_certificate_info(api_token, tenant_id, user_id, pki, digest_b64):
    url = PPLG_DOMAIN_URL + '/api/openapi/sdk-sign-info.json'
    body = {
        'tenant_id': tenant_id,
        'pki': pki,
        'user_id': user_id,
        'digest_b64': digest_b64
    }
    headers = {
        'X-Paperlogic-Authorization': api_token,
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return True, data['result']
    else:
        print("Error")
        return False, response.text

def pplg_request_user_info(api_token, tenant_id, user_id, email):
    url = PPLG_DOMAIN_URL + '/api/openapi/sdk-user-info.json'
    body = {
        'tenant_id': tenant_id,
    }
    
    if user_id:
        body['user_id'] = user_id
    elif email:
        body['email'] = email
    
    headers = {
        'X-Paperlogic-Authorization': api_token,
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return True, data['result']
    else:
        print("Error")
        return False, response.text


async def prep_document(input_file, field_name, reason):
    ext_signer = signers.ExternalSigner(
        signature_value = bytes(256),
        signing_cert    = None,
        cert_registry   = None,
    )
    pdf_signer = signers.PdfSigner(
        signers.PdfSignatureMetadata(
            md_algorithm='sha256',
            reason=reason,
            field_name=field_name, 
        ),
        signer=ext_signer,
    )

    pdf_buffer = open(input_file, 'rb')
    w = IncrementalPdfFileWriter(pdf_buffer)
    prep_digest, _, output_handle = await pdf_signer.async_digest_doc_for_signing(w, bytes_reserved=BYTES_RESERVED)

    return prep_digest, output_handle

async def proceed_with_signing(
        input_file, field_name, prep_digest, output_handle, 
        signature, certificate, 
        timestamp_url, timestamp_username, timestamp_password
    ):
    
    timestamper = timestamps.HTTPTimeStamper(
        timestamp_url,
        auth=HTTPBasicAuth(timestamp_username, timestamp_password)
    )

    cert_registry = SimpleCertificateStore()

    ext_signer = signers.ExternalSigner(
        signing_cert    = certificate,
        signature_value = signature,
        cert_registry   = cert_registry,
        embed_roots     = True,
    )

    signed_attrs = await ext_signer.signed_attrs(
        prep_digest.document_digest, 'sha256', use_pades=True
    )

    sig_cms = await ext_signer.async_sign_prescribed_attributes(
        'sha256', signed_attrs=signed_attrs,
        timestamper=timestamper
    )

    validation_context = ValidationContext(
        allow_fetching=True,
    )

    pdf_signer = signers.PdfSigner(
        signers.PdfSignatureMetadata(
            field_name=field_name, 
            embed_validation_info=True, use_pades_lta=True,
            subfilter=fields.SigSeedSubFilter.PADES,
            validation_context=validation_context,
            md_algorithm='sha256',
            dss_settings=DSSContentSettings(include_vri=False),
        ),
        signer=ext_signer,
    )

    pdf_buffer = open(input_file, 'rb')
    w = IncrementalPdfFileWriter(pdf_buffer)
    _, tbs_document, _ = await pdf_signer.async_digest_doc_for_signing(w)

    psi = tbs_document.post_sign_instructions
    
    await PdfTBSDocument.async_finish_signing(
        output_handle, prepared_digest=prep_digest,
        signature_cms=sig_cms,
        post_sign_instr=psi,
        validation_context=validation_context
    )

async def full_procedure(input_file, output_file, api_token, tenant_id, pki, user_id, email):
    field_name = 'Signature1'
    
    # 0. Get user_info for reason
    check_user_info, user_info = pplg_request_user_info(api_token, tenant_id, user_id, email)
    if not check_user_info:
        print('Error: get user info')
        return 

    formatted_datetime_str = format_date()
    reason = [
        'Date Time: %s' % formatted_datetime_str,
        'Signer Name: %s' % user_info['user_full_name'],
        'Company Name: %s' % user_info['user_company_name'],
        'Division: %s' % (user_info['division'] if user_info['division'] is not None else ''),
        'Email: %s' % user_info['user_email'],
    ]
    reason_text = ', '.join(reason)

    # 1. Prepare document and signed attributes to sign
    prep_digest, output = await prep_document(input_file, field_name, reason_text)
    ## encode digest to base64
    digest_b64 = base64.b64encode(prep_digest.document_digest).decode('utf-8')

    # 2. Remote signing service
    user_id = user_info['user_id']
    check_signing_response, signing_response = pplg_request_certificate_info(api_token, tenant_id, user_id, pki, digest_b64)
    if not check_signing_response:
        print('Error: get certificate info')
        return 
    
    ## decode response
    signature = base64.b64decode(signing_response['signature'])
    certificate = x509.Certificate.load(
        base64.b64decode(signing_response['certificate'])
    )

    timestamp_info = json.loads(decrypt_data(signing_response['_t'], api_token).decode('utf-8'))
    timestamp_url = timestamp_info['ts_url']
    timestamp_username = timestamp_info['ts_username']
    timestamp_password = timestamp_info['ts_password']

    # 3. Finish signing
    await proceed_with_signing(
        input_file, 
        field_name, 
        prep_digest, 
        output, 
        signature, 
        certificate, 
        timestamp_url,
        timestamp_username,
        timestamp_password
    )

    with open(output_file, 'wb') as f:
        f.write(output.getbuffer())

def sign_pplg(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None):
    asyncio.run(full_procedure(input_file, output_file, api_token, tenant_id, pki, user_id, email))

