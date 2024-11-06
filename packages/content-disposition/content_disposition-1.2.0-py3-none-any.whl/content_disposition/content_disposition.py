import unicodedata
from urllib.parse import quote

__all__ = [
    "rfc5987_content_disposition",
]


def rfc5987_content_disposition(file_name, disposition_type="inline"):
    """
    Set content headers according to RFC 5987

    :param file_name: str|unicode
    :param disposition_type: str
    :return:
    """
    ascii_name = (
        unicodedata.normalize("NFKD", file_name).encode("ascii", "ignore").decode()
    )
    header = f'{disposition_type}; filename="{ascii_name}"'
    if ascii_name != file_name:
        quoted_name = quote(file_name)
        header += f"; filename*=UTF-8''{quoted_name}"

    return header
