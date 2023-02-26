""" ToDo:

    ☑ add multi-threading
    ☐ add timers

"""

from Sorters import Quicksort, Bubble, Mergesort
import concurrent.futures as fut


class Sorter():
    def __init__(self, chosen_sorters=[]):
        self.sorters = self.createSorters(chosen_sorters)

    def createSorters(self, chosen_sorters):
        result = []
        sorters = {"quicksort":Quicksort, "bubble":Bubble, "mergesort":Mergesort}

        for chosen in chosen_sorters:
            result.append( sorters[chosen]() )

        return result

    # add multi-threading
    def sort(self, content):
        p = fut.ProcessPoolExecutor()
        toSort = self.parseContentList(content)

        future_threads = [p.submit(sorter.sort, toSort.copy()) for sorter in self.sorters]

        res = []
        for r in fut.as_completed(future_threads):
            res.append(r.result())
        
        for i in range(len(self.sorters)):
            print(self.sorters[i], res[i][1])


    def parseContentList(self, _list):
        """
        Accepted formats:
            -string of numbers:
                "12345"

            - csv
                "a,1\nb,2\nc,3\nd,4\ne,5\n"

            - string with comma separated values (with or without brackets):
                "1,2,3,4,5"
                "[1,2,3,4,5]"

            - string with key-value pairs (with or without curly brackets (json)):
                "a:1, b:2, c:3, d:4, e:5"
                "{a:1, b:2, c:3, d:4, e:5}"
            
            - column of numbers:
                1\n2\n3\n4\n5
        
        returns list of tuples:
            [(a,1), (b,2), (c,3), (d,4), (e,5)]
        """

        # Mejorar validaciones
        def detect_format(content):
            if ":" in content: return "dict"
            if "\n" in content and not "," in content: return "column"
            if "\n" in content: return "csv"
            if "," in content: return "list"
            try:
                int(content) 
                return "string"
            except ValueError: return "invalid"

        _format = detect_format(_list)
        _list = _list.translate(str.maketrans('', '', ' '))

 
        result={}
        if _format == "csv":
            _list = _list.split("\n")
            result = [tuple((i.split(","))) for i in _list ]

        elif _format == "dict":
            _list = _list.translate(str.maketrans('', '', '}{\n'))
            _list = _list.split(",")

            result = [( i.split(":")[0], int(i.split(":")[1]) ) for i in _list if "" not in i.split(":") ]

        elif _format == "list":
            _list = _list.translate(str.maketrans('', '', '[]'))
            _list = _list.split(",")
            result = [(i,int(_list[i])) for i in range(len(_list))]
        elif _format == "string":
            _list = _list.split("")
            result = [(i,int(_list[i])) for i in range(len(_list))]
        elif _format == "column":
            _list = _list.split("\n")
            result = [(i,int(_list[i])) for i in range(len(_list))]
        elif _format == "invalid":
            raise Exception()
        else:
            raise Exception()
        
        return result
