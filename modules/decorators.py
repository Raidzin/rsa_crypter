class CheckDecorators:
    def check_files(self, func, error_lbl, *args):
        empty_files = [file for file in args if not hasattr(self, file)]
        error_lbl.setText()
