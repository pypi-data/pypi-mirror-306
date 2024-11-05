class EncryptionNotSetException(Exception):
    def __str__(self):
        return (
            "Encryption not set. Please refer to our encryption documentation  "
            "https://docs.aqarios.com/get-started#luna-encryption for more information."
        )
