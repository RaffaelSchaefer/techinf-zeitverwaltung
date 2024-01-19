def error_handling(func: function):
    def wrapper():
        try:
            func()
        except Exception as e:
            return {
                "error": str(e)
            }, 400
    return wrapper
