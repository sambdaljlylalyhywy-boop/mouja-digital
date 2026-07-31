import os


def delete_file(file_path: str):
    """
    حذف ملف بعد الانتهاء من استخدامه
    """

    try:
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        pass


def get_file_size(file_path: str):
    """
    إرجاع حجم الملف بالميجابايت
    """

    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return round(size / (1024 * 1024), 2)

    return 0
