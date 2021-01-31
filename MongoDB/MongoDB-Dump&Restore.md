# MongoDB - Dump & Restore

새로운 DB로옮겨가면서 기존 DB를 dump뜨고 새로운 DB에 Dump뜬데이터를 Restore 하는 작업이 필요하다

* 현재 운영 DB 주소: 192.1.x.x:27017 ( A )
   * user: abc / pwd: abc123
* 이전할 DB 주소: 192.2.x.x:27100 ( B )
   * user: efg / pwd efg123 

## 1. 현재 운영중인 DB에서 dump 진행

~~~
server@root $ mongodump --out ./ --host 192.1.x.x --port 27017 -u 'abc' -p 'abc123' --authenticationDatabase admin --db DB_NAME

server@root $ nohup mongodump --out ./ --host localhost --port 27017 -u abc -p 'abc123' --authenticationDatabase admin --db DB_NAME > ./dumplog.out &

-collection 따로 dump
server@root $ nohup mongodump --out ./ --host localhost --port 27017 -u abc -p 'abc123' --authenticationDatabase admin --db DB_NAME --collection collection_name -q '{"collect_day": {$gte: "20220110", $lte: "20220125"}}' > ./dumplog_collection.out &
~~~
<sup> collection따로 지정시 -q {collect_day}컬럼이 컬렉션안에 있어서 그기간으로 지정</sup>

 
* option
  * --out :  dump파일을 어디에다 만드는지 경로 ./
default는 nohup.out이 생기는데, > ./파일명.out하면 여기로 생김 그리고 마지막에 &
  * --numParallelCollections int, -j int
 기본 4개덤프인데, 옵션으로 더할수잇음, 
  *  \> .dumplog.out & : 같은경로에서 덤프실행시 같은파일에서 log를쌓기때문에 따로 지정해줌 


## 2. MongoDB Restore
~~~
server@root
nohup mongorestore -h 192.2.x.x:27100 -d DB_NAME -c collection_name -u efg -p efg123 --authenticationDatabase admin --numInsertionWorkersPerCollection 4 --noIndexRestore ./DB_NAME/collection_name.bson > ./collection_name_restore.out &
~~~


## Mongo export & import
데이터를 내보내고 가져오는 다른방법
~~~
#exoprt

$ mongoexport -d databaseName -c collectionName -o output.json --port 27017
~~~
* -d : 추출하고자 하는 Database 이름을 입력
* -c : 추출하고자 하는 Collection 이름을 입력
* -o : 추출한 결과를 저장할 파일의 이름
* --port :  현재 돌고 있는 MongoDB 중 추출하고자 하는 MongoDB의 포트번호를 입력

~~~
#import
$ mongoimport -d databaseName -c collectionName --file output.json --jsonArray --port 27017
~~~
* --file : import 하기 위해 데이터가 저장되어 있는 파일 위치
* --jsonArray : file이 json 형태로 구성되어 있는 경우에 사용

> (참고)  https://docs.mongodb.com/v4.0/reference/program/mongodump/index.html 