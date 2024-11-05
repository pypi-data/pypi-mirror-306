import os
import requests
import mlflow

JUPYTER_USER_ENV = "JUPYTERHUB_USER"

def check_user(experiment_name):
    if experiment_name is None:
        print("Experiment Name은 반드시 설정하여야 합니다. 만약 생성하지 않은 경우, Experiment -> New Experiment 를 통해 생성하여주시기 바랍니다.")
        return False

    user = os.getenv(JUPYTER_USER_ENV)
    if user is None:
        print("사용자 검증 중 Notebook 정보가 누락되었습니다. 해당 Notebook을 삭제하고, 새로운 Notebook을 생성하여 다시 시도하여 주세요.")
        return False

def process(model_function,
            experiment_name=None,
            tracking_server_url="http://mlflow-svc.mlflow-system.svc.cluster.local:5001",
            core_server_url: str = "http://core-server-svc.core-system.svc.cluster.local:8080",
            model_type: str = "keras"):
    # 유효한 유저인지 확인합니다.
    # TODO: 여기서 user_id 뿐만 아니라 UserDto를 가져오는 형식으로 해야함
    user = request_get_user_id()
    # 사용자가 생성한 Experiment가 존재하는지 확인합니다.
    if experiment_name is None:
        print("Experiment Name은 반드시 설정하여야 합니다.")
        return
    
    print("MLFlow 사전 설정을 시작합니다.")
    mlflow.set_tracking_uri(tracking_server_url)
    print(f"MLFlow Server URL: {tracking_server_url}")

    experiment = None
    if experiment_name is not None:
        print(f"Experiment Name을 '{experiment_name}'로 설정합니다.")
        experiment = mlflow.set_experiment(experiment_name=experiment_name)

    mlflow.start_run()

    experiment_id = experiment.experiment_id
    run_id = extract_run_id()

    if (model_type == 'keras'):
        mlflow.keras.autolog()
    elif (model_type == 'tensorflow'):
        mlflow.tensorflow.autolog()
    elif (model_type == 'sklearn' or model_type == 'scikit-learn'):
        mlflow.sklearn.autolog()
    else:
        mlflow.autolog()

    mlflow.log_artifact('metrics.txt', artifact_path='metrics')
    try:
        model_function()
    except Exception as e:
        print('예외 발생', e)
        run_id = mlflow.active_run().info.run_id
        mlflow.end_run(status='FAILED')
        mlflow.delete_run(run_id)
        return
    mlflow.end_run()
    request_create_run(experiment_id=experiment_id,
                       core_server_url=core_server_url,
                       run_id=run_id,
                       email=user.get('email'))

    # Core Server로 요청 보내기 with run_id

def extract_run_id():
    run = mlflow.active_run()
    return run.info.run_id

def request_create_run(experiment_id: str,
                       run_id: str,
                       email: str,
                       core_server_url: str = "http://core-server-svc.core-system.svc.cluster.local:8080",
                       api: str = "/experiment/runs/"):
    
    data = {
        "experiment_id" : experiment_id,
        "run_id" : run_id
    }

    cookies = {
        'authenticated_email' : email
    }

    requests.post(core_server_url+api, json=data, cookies=cookies)

def request_get_user_id(core_server_url: str = "http://core-server-svc.core-system.svc.cluster.local:8080",
                        api: str = "/notebook/user/"):
    notebook_id = os.environ.get("JUPYTERHUB_USER")
    api_url = f"{core_server_url}{api}"
    params = { 'notebook_id' : notebook_id }

    response = requests.get(api_url, params=params)
    user = response.json()
    # user_id = data.get('user_id')
    return user
    
