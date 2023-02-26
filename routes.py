""" ToDo:

    - add support for multiple file upload

"""

from aiohttp.web import View, RouteTableDef, Response, FileResponse
import os

from Sorter import Sorter


routes = RouteTableDef()

@routes.view('/')
@routes.view('/index.html')
class Index(View):

    async def get(self):
        path = os.path.dirname(__file__)
        return FileResponse(path=path + '/html/index.html', status=200)

    async def post(self):
        data = await self.request.post()

        items = data["items"]

        sorter_choices = ["quicksort", "bubble", "mergesort"]
        chosen_sorters = [s for s in sorter_choices if s in data]

        if not sorter_choices: return Response(text="no sorter chosen", status=501)

        txt_file = items.file
        content = txt_file.read().decode("utf-8")

        sorter = Sorter(chosen_sorters=chosen_sorters)
        sorter.sort(content)

        print(chosen_sorters)
        return Response(text=str(chosen_sorters), status=200)
