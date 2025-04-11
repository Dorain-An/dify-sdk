from .const_basic import DocStrEnum


class DocumentType(DocStrEnum):
    TXT = ("TXT", "txt")
    PDF = ("PDF", "pdf")
    MD = ("MD", "md")
    MARKDOWN = ("MARKDOWN", "markdown")
    HTML = ("HTML", "html")
    XLSX = ("XLSX", "xlsx")
    XLS = ("XLS", "xls")
    DOCX = ("DOCX", "docx")
    CSV = ("CSV", "csv")
    EML = ("EML", "eml")
    MSG = ("MSG", "msg")
    PPTX = ("PPTX", "pptx")
    PPT = ("PPT", "ppt")
    XML = ("XML", "xml")
    EPUB = ("EPUB", "epub")


class ImageType(DocStrEnum):
    PNG = ("PNG", "png")
    JPEG = ("JPEG", "jpeg")
    JPG = ("JPG", "jpg")
    GIF = ("GIF", "gif")
    WEBP = ("WEBP", "webp")
    SVG = ("SVG", "svg")


class AudioType(DocStrEnum):
    MP3 = ("MP3", "mp3")
    M4A = ("M4A", "m4a")
    WAV = ("WAV", "wav")
    WEBM = ("WEBM", "webm")
    ARM = ("ARM", "arm")


class VideoType(DocStrEnum):
    MP4 = ("MP4", "mp4")
    MOV = ("MOV", "mov")
    MPEG = ("MPEG", "mpeg")
    MPGA = ("MPGA", "mpga")


class TransferMethod(DocStrEnum):
    URL = ("remote_url", "图片地址")
    FILE = ("local_file", "上传的文件")
