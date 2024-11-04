Example for test Make Circle

    from electf4 import tdd
    
    tdd.tdd_make_circles()

Example for use this package

    from electf4 import make_circles as mc
    from electf4 import make_confusion_matrix as mm
    labels_name = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eigth", "nine"]
    mm(y_true = y_test,
        y_pred = y_preds,
        classes = labels_name,
        figsize = (11, 11),
        text_size = 7)
