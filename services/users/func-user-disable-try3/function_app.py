import azure.functions as func
import logging

# from project.process_management import inspection_process_management


app = func.FunctionApp()


@app.function_name(name="HttpTrigger1")
@app.route(route="")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')
        # inspection_process_management()
    except Exception:
        logging.info("Exception")
    return func.HttpResponse(
        "finish",
        status_code=200
    )
