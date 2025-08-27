from enum import Enum


class Margins(Enum):
    """
    Enum to centralize and manage document margin settings.
    Using an Enum ensures consistent values across the application.
    """
    ALL = 0.5


class Dimensions(Enum):
    """
    Enum to define fixed dimensions for document generation.
    It includes standard paper sizes and image dimensions to ensure
    consistency when creating documents.
    """
    HEIGHT = 297  # A4 Height in Millimeters
    WIDTH = 210  # A4 Width in Millimeters
    IMG_WIDTH = 7  # 7 Inches


class FolderName(Enum):
    """
    Enum to provide consistent names for application-generated folders.
    This helps prevent typos and centralizes the folder naming logic.
    """
    IMG_FOLDER_NAME = "generated_images"
    DOC_FOLDER_NAME = "generated_docs"
