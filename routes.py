from aiohttp.web import View, RouteTableDef, Response, FileResponse, HTTPTemporaryRedirect
import os
import concurrent.futures as fut
from exceptions import InternalServerError

from Sorter import Sorter


def getRoutes(file_dir):

    routes = RouteTableDef()

    sorting_choice = """
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="index.css">
    </head>
    <center>
    <form method="post" accept-charset="utf-8" enctype="multipart/form-data">
    <br>
    <label class="subtitle" >Select sorting method:</label>
    <br>

    <br>

    <input id="quicksortChoice" type="checkbox" value="True" name="quicksort"/>
    <label class="list_item" for="quicksortChoice">Use Quick Sort</label>

    <br>

    <input id="bubbleChoice"    type="checkbox" value="True" name="bubble"/>
    <label class="list_item" for="bubbleChoice">Use Bubble Sort</label>

    <br>

    <input id="mergesortChoice" type="checkbox" value="True" name="mergesort"/>
    <label class="list_item" for="mergesortChoice">Use Merge Sort</label>

    <br>
    <br>
    <br>

    <label class="subtitle" >Select file to sort:</label>
    <br>
    <br>
    """


    @routes.view('/')
    @routes.view('/index.html')
    class Index(View):

        async def get(self):
            path = os.path.dirname(__file__)
            return FileResponse(path=path + '/html/index.html', status=200)

        async def post(self):
            path = os.path.dirname(__file__)
            data = await self.request.post()

            items = data["items"]

            if hasattr(items, "file"):
                p_file = items.file
                content = p_file.read().decode("utf-8")
                new_f = open(path+file_dir+items.filename, "w")

                new_f.write(content)
            else:
                return Response(text="no file chosen", status=501)

            return HTTPTemporaryRedirect("/explorer")


    @routes.view("/index.css")
    class css(View):
        async def get(self):
            path = os.path.dirname(__file__)
            return FileResponse(path=path+"/html/index.css")


    @routes.view("/explorer")
    class explorer(View):
        async def get(self):
            p = fut.ProcessPoolExecutor()

            path = os.path.dirname(__file__)
            data = await self.request.post()
            url = str(self.request.url)
            print(data.values())
            if "file" in data:
                items = data["file"]

            params = url[url.find("?")+1:]
            print(params)
            if "=" in params:
                file = params.split("=")
                print(file)
                file = file[1]

                if file.endswith(".py"):
                    py = open(path+file_dir+file)
                    
                    p.submit(exec, py.read(),{"__file__":os.path.dirname(__file__)+file_dir})
                    res = self.makelist()
                    return Response(content_type="text/html", text=res, status=200)

                content = open(path+file_dir+file, "r")
                return FileResponse(path=path+file_dir+file)

            res = self.makelist()

            return Response(content_type="text/html", text=res, status=200)


        async def post(self):

            path = os.path.dirname(__file__)
            data = await self.request.post()

            if not "file" in data:
                res = self.makelist()
                return Response(content_type="text/html", text=res, status=200)

            sorter_choices = ["quicksort", "bubble", "mergesort"]
            chosen_sorters = [s for s in sorter_choices if s in data]

            #if not sorter_choices: return Response(text="no sorter chosen", status=501)

            file = data["file"]
            p_file = open(path+file_dir+file, "r")

            content = p_file.read()

            sorter = Sorter(chosen_sorters=chosen_sorters)

            try:
                res = sorter.sort(content)
                return Response(content_type="text/html", text=self.resultHTML(res), status=200)
            except InternalServerError:
                return Response(content_type="text/html", text="<center><h3>the uploaded file is not supported</h3></center>", status=500)


        def makelist(self):
            files = os.listdir("."+file_dir)
            res = sorting_choice

            if files == []:
                res+="<p> there are no files in storage to sort </p>"


            for f in files:
                res+='<input type="radio" value="'+f+'" name="file"/>'+'<label for="'+f+'">'+'<a href="explorer?file={}">{}</a>'.format(f,f, f)+'</label><br>'

            res += '<br><input type="submit" value="Sort File" name="submit"/><br><br>' + "</form></center></body></html>" 
            return res


        def resultHTML(self, res):

            timer_results = ""
            table = "<table><tr><th>Original List</th>"
            for s in res[0]:
                timer_results += "<p>{} tardo: {}</p><br>".format(s[2], s[1])

                table+="<th>"+s[2]+"</th>"
            table+="</tr>"

            n = len(res[1])
            for i in range(n):
                table += "<tr><td>"+str(res[1][i])+"</td>"
                for s in res[0]:
                    table+= "<td>"+str(s[0][i])+"</td>"


            table+="</table>"
            html = """<!DOCTYPE html><html><head><link rel="stylesheet" href="index.css"></head><body>{}<br><br>{}</body></html>""".format(timer_results, table)
            return html
    
    return routes