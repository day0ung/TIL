
# MySql - Index

## INDEX
인덱스는 테이블의 동작속도(조회)를 높여주는 자료구조이다. 인덱스로 데이터의 위치를 빠르게 찾아주는 역할을 한다.

인덱스는 MYI(MySQL Index)파일에 저장되며, 인덱스가 설정되지 않았다면 Table Full Scan이 일어나 성능이 저하되거나 치명적인 장애가 발생한다.

조회속도는 빨라지지만 UPDATE, INSERT, DELETE의 속도는 저하된다는 단점이 있다. (Table의 index 색인 정보를 갱신하는 추가적인 비용 소요)  
즉, 너무많은 인덱스생성은 성능저하의 원인이 된다.

## 효율적인 인덱스 설계방법
* 무조건 많이 설정하지 않는다. (한 테이블당 3~5개가 적당 목적에 따라 상이)
* 조회시 자주 사용하는 컬럼
* 고유한 값 위주로 설계
* 카디널리티가 높을 수록 좋다 (= 한 컬럼이 갖고 있는 중복의 정도가 낮을 수록 좋다. 예를들어 주민등록번호같은거)
* INDEX 키의 크기는 되도록 작게 설계
* PK, JOIN의 연결고리가 되는 컬럼
* 단일 인덱스 여러 개 보다 다중 컬럼 INDEX 생성 고려
* UPDATE가 빈번하지 않은 컬럼
* JOIN시 자주 사용하는 컬럼
* INDEX를 생성할 때 가장 효율적인 자료형은 정수형 자료(가변적 데이터는 비효율적)

## INDEX 문법
### 인덱스 조회
~~~sql
SHOW INDEX FROM TABLE_NAME
~~~

### 인덱스 생성
~~~sql
-- 단일 인덱스
CREATE INDEX 인덱스이름 ON 테이블이름(필드이름1)

-- 다중 컬럼 인덱스
CREATE INDEX 인덱스이름 ON 테이블이름(필드이름1, 필드이름2, ...)
~~~

### UNUQUE 인덱스 생성(중복 값을 허용하지 않는 인덱스)
~~~sql
-- 단일 인덱스
CREATE UNIQUE INDEX 인덱스 이름 ON 테이블이름(필드이름1)
-- 다중 컬럼 인덱스
CREATE UNIQUE INDEX 인덱스 이름 ON 테이블이름(필드이름1, 필드이름2, ...)
~~~


### 인덱스 삭제
~~~sql
ALTER TABLE 테이블이름 DROP INDEX 인덱스이름;
~~~

### 인덱스 추가
~~~sql
ALTER TABLE 테이블이름 ADD (UNIQUE)INDEX 인덱스이름(컬럼명1, 컬럼명2...);
~~~

### 운영중인 테이블에 인덱스를 추가로 생성할시 LOCK걸리지 않게 옵션추가
~~~sql
ALTER TABLE `테이블이름` ADD INDEX `인덱스이름` (`컬럼명1`) , ALGORITHM=INPLACE, LOCK=NONE;

~~~
* <a href = "https://dev.mysql.com/doc/refman/8.0/en/create-index.html"> Mysql 인덱스 생성시 옵션참고 </a>
~~~sql
CREATE [UNIQUE | FULLTEXT | SPATIAL] INDEX index_name
    [index_type]
    ON tbl_name (key_part,...)
    [index_option]
    [algorithm_option | lock_option] ...

key_part: {col_name [(length)] | (expr)} [ASC | DESC]

index_option: {
    KEY_BLOCK_SIZE [=] value
  | index_type
  | WITH PARSER parser_name
  | COMMENT 'string'
  | {VISIBLE | INVISIBLE}
  | ENGINE_ATTRIBUTE [=] 'string'
  | SECONDARY_ENGINE_ATTRIBUTE [=] 'string'
}

index_type:
    USING {BTREE | HASH}

algorithm_option:
    ALGORITHM [=] {DEFAULT | INPLACE | COPY}

lock_option:
    LOCK [=] {DEFAULT | NONE | SHARED | EXCLUSIVE}
~~~


### 테이블 생성시 인덱스 추가 (예시)
~~~sql
CREATE TABLE `PRODUCT` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `PRODUCT_ID` bigint(20) DEFAULT NULL,
  `OPTION` varchar(50) DEFAULT NULL,
  `PRICE` int(11) DEFAULT NULL,
  `COLLECT_DAY` varchar(18) DEFAULT NULL,
  `REG_ID` varchar(18) DEFAULT NULL,
  `REG_DT` datetime NOT NULL,
  PRIMARY KEY (`ID`,`REG_DT`),
  KEY `IX_PRODUCT_1` (`PRODUCT_ID`),
  KEY `IX_PRODUCT_2` (`PRODUCT_ID`,`COLLECT_DAY`),
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
~~~

* <a href="https://hoing.io/archives/7909"> 참고URL </a>

