# -*- encoding: utf-8 -*-
'''
run_dev.py
----
start a dev server


@Time    :   2024/01/16 10:08:06
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app.main:app', host="localhost", port=8080, reload=True)
