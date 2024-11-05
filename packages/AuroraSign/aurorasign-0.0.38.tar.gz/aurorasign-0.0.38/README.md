# 1. Sign PDF:
```python
    from AuroraSign import sign
    
    api_key = 'abc'
    tenant_id = 1
    cert_type = 1
    input_file = 'contract-1.pdf'
    output_file = 'contract-1-signed.pdf'

    sign(input_file, output_file, api_key, tenant_id, cert_type)
```