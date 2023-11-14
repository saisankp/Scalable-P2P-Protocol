from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta

def generate_self_signed_certificate():
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, u'Certificate'),
    ])
    certificate = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())

    return private_key, certificate

def save_to_pem(private_key, certificate):
    # Save private key to PEM file
    with open('private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save certificate to PEM file
    with open('certificate.pem', 'wb') as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.PEM
        ))

if __name__ == "__main__":
    private_key, certificate = generate_self_signed_certificate()
    save_to_pem(private_key, certificate)
    print("Certificate and private key saved as certificate.pem and private_key.pem")
