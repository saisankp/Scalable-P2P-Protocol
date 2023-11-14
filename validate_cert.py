from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography import x509

def load_private_key():
    # Load private key from PEM file
    with open('private_key.pem', 'rb') as f:
        private_key_data = f.read()
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
            backend=default_backend()
        )
    return private_key

def load_certificate():
    # Load certificate from PEM file
    with open('certificate.pem', 'rb') as f:
        cert_data = f.read()
        certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
    return certificate

def verify_certificate(private_key, certificate):
    # Verify the certificate
    try:
        public_key = certificate.public_key()
        public_key.verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificate.signature_hash_algorithm,
        )
        print("Certificate is valid.")
    except Exception as e:
        print(f"Certificate verification failed: {e}")

if __name__ == "__main__":
    private_key = load_private_key()
    certificate = load_certificate()
    verify_certificate(private_key, certificate)
