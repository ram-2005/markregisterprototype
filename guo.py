  if clsdetails[0] in ("class11\n", "class12\n"):
                if cls[3] == "biomaths\n":
                    tablename = tablename + "biomaths" +"teachertable"
                elif cls[3] == "computermath\n":
                    tablename = tablename + "biomaths" +"teachertable"
                elif cls[3] == "commerce\n":
                    clsinfo = ["class teacher", "english", "computer", "accounts", "buissness", "economics"]
            elif cls[0][-2] in ("3", "4", "5", "6", "7", "8", "9", "0",) and cls[0][-3] in ("s", "1",):
                widget.setCurrentIndex(17)
            elif cls[0][-2] in ("1", "2") and cls[0][-3] in ("s"):
                widget.setCurrentIndex(17)
