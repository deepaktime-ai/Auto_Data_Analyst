def safe_execute(func, *args, **kwargs):
    """
    Safely execute any function and catch errors
    """
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        return None, str(e)


def format_error(error_msg):
    """
    Clean error formatting
    """
    return f"❌ Error: {error_msg}"


def validate_column(df, column):
    """
    Check if column exists in dataframe
    """
    if column not in df.columns:
        return False, f"Column '{column}' not found in dataset."
    return True, None