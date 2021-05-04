# ベースイメージの指定
FROM python:3.8

# ソースを置くディレクトリを変数として格納                      
ARG project_dir=/projects/

# 必要なファイルをローカルからコンテナにコピー
ADD src/requirements.txt $project_dir
ADD src/app.py $project_dir

# requirements.txtに記載されたパッケージをインストール
WORKDIR $project_dir
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# flaskを実行
ENV FLASK_APP app.py
#開発中は自動起動せず、コンテナ内に入って手動で起動する。コマンドはREADME.md参照
#CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
