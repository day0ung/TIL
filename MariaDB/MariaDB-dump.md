# MariaDB - Dump

## [pv install]
yum install -y pv

## [Database 용량 확인]
SELECT table_schema AS "Database", ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" FROM information_schema.TABLES GROUP BY table_schema;

## [MySQL 스키마 덤프(+진행률)]
mysqldump -uroot -p패스워드 -d DB명 | pv --progress --size 용량 > 덤프파일명.sql

~~~
ex) 
mysqldump -uroot -ppassword -d jdy_db | pv --progress --size 100m > jdy_db.sql
~~~

## [MySQL 복원(+진행률)]
pv 덤프파일명.sql | mysql 대상DB명

~~~
pv jdy_db.sql | mysql jdy_new
~~~


## [MySQL 원격 덤프]

mysqldump -u유저명 -p패스워드명 -h '호스트(IP)' DB명 TABLE명(생략가능) > 덤프파일명.sql
~~~
mysqldump --user=jdy --password='jdy!23' -h 133.186.143.96 jdy_db TABLE_USER > dump.sql 
~~~


**주의점**  
<sup> 원격지점에 보안그룹 설정 확인
스키마 덤프가 아닌 데이터 덤프시 테이블 트랜잭션 확인필요(해당 테이블 사용중이라면 --single-transaction 옵션 추가)
데이터만 뜨면서 create문 필요 없을 때 --no-create-info 옵션 추가</sup>


## [MySQL 조건 덤프]

mysqldump -u유저명 -p패스워드명(패스워드 없으면 생략가능) DB명 TABLE명 --where="조건 컬럼 >= 조건 AND 조건컬럼 < 조건 " > dump.sql

~~~
ex)
mysqldump -uroot jdy_db TABLE_NAME --where="REG_DT >='2022-01-01' AND REG_DT < '2022-02-01' " > ivt_2022-01-01_2022-01-31.sql
~~~


##[AUTO_INCREMENT 초기화]

스키마 덤프 후에 실행 할 수 있다.

$vi 덤프파일명.sql

:%s/AUTO_INCREMENT=\+[0-9]\+/AUTO_INCREMENT=1 입력 후 엔터