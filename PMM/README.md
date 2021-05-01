# PMM

Percona Monitoring and Management (PMM)는 무료 오픈 소스 Database 통합 모니터링 솔루션이다.

PMM 클라이언트 패키지 구성

- pmm-admin : 모니터링할 데이터베이스 인스턴스를 추가 및 제거 등 PMM 클라이언트를 관리하기 위한 명령줄 도구
- pmm-agent : 클라이언트 인증을 수행하고 PMM 서버에 저장된 클라이언트 구성을 가져오고 내보내기 및 기타 에이전트를 관리
- exporter : 각 시스템의 노드 또는 DB 메트릭을 수집하는 도구

# Local서버에 PMM Server 설치 
~~~
# yum-config-manager 사용하기 위해 yum-utils설치 
sudo yum -y install yum-utils

# 레포지토리 설치
sudo --add-repo https://download.docker.com/linux/centos/docker-ce.repo
 
# Docker 설치 및 구동 
sudo yum -y install docker-ce
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# 이미지 받아오기
docker pull percona/pmm-server:2

# 영구 데이터 컨테이너 생성 
docker create --volume /srv \
--name pmm-data \
percona/pmm-server:2 /bin/true

# PMM 서버 시작
docker run --detach --restart always \
--publish 443:443 \
--volumes-from pmm-data \
--name pmm-server \
percona/pmm-server:2

* client server : 211.38.5.156
* mongo server : 133.x.x.x

* pmm-server/client연결시 라우트설정 해주어야함 
~~~

# DB 서버에서 PMM Client 설치 
### 1. PMM Client 설치 
~~~
$ sudo yum -y install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
$ sudo yum -y install pmm2-client
~~~

### 2. PMM Server 에 Client 등록 
~~~
$ sudo pmm-admin config --server-insecure-tls --server-url=https://admin:admin@211.38.5.156:4333 133.x.x.x generic mongo-mr-mongos-1

$ sudo pmm-admin add mongodb --username=pmm_mongodb --password=password --service-name=mongo-mongos --host=127.0.0.1 --port=27100
~~~
* <code>$ pmm-admin list</code> 제대로 설정되었다면 명령어로확인
* ![](./img/pmm-admin%20list.png)

### MongoDB에 DB 모니터링 계정 생성 
~~~sql
db.getSiblingDB("admin").createRole({
    role: "explainRole",
    privileges: [{
        resource: {
            db: "",
            collection: ""
            },
        actions: [
            "listIndexes",
            "listCollections",
            "dbStats",
            "dbHash",
            "collStats",
            "find"
            ]
        }],
    roles:[]
})

db.getSiblingDB("admin").createUser({
   user: "pmm_mongodb",
   pwd: "password",
   roles: [
      { role: "explainRole", db: "admin" },
      { role: "clusterMonitor", db: "admin" },
      { role: "read", db: "local" }
   ]
})
~~~

## 설정 완료시
| HOME_DashBoard      |  Cluster_DashBoard |
| ---------- | ------------- 
|![](./img/home_dashboard.png) | ![](./img/mogno_dashboard.png)| 