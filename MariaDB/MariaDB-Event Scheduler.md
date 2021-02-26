# Event Scheduler

Scheduler를 사용하기 위해 Event Scheduler를 사용
JAVA의 쿼츠(Quartz), 리눅스의 크론탭(Linux Crontab)을 사용해도 되지만 MySQL도 스케줄러 이벤트 기능을 사용할수있다.


### 1. event가 자동으로 실행되도록 하기 위해서는 event_scheduler 변수를 ON
~~~
SET GLOBAL event_scheduler = ON;
~~~

* event_scheduler 변수를 영구적으로 ON 설정하고 싶은 경우 my.cnf 파일의 [mysqld]에 event_scheduler = on을 꼭 추가

### 2. 반복 실행하고 싶은 쿼리를 반복 주기와 함께 이벤트로 생성한다.
~~~sql
CREATE EVENT testing -- EVENT명을 지정한다.
    ON SCHEDULE
        EVERY 10 second -- Event 실행 주기
        STARTS '2019-05-11 19:45:00' -- Event 최초 시작 시간
    DO
        insert into testing(insertTime) values(now()); -- 실행 쿼리문


--한번만 하고싶은경우
CREATE EVENT testing -- EVENT명을 지정한다.
    ON SCHEDULE AT '2019-05-11 19:45:00'
    DO
        insert into testing(insertTime) values(now()); -- 실행 쿼리문
[출처] [MariaDB(마리아디비)] 이벤트 스케쥴러(Event Scheduler)로 지정한 시간에 자동 insert/delete 하기|작성자 천프로
~~~

### 이벤트 관련 query
~~~
[이벤트 목록 보기]
SHOW EVENTS
SELECT * FROM information_schema.EVENTS;

[이벤트 삭제]
DROP event my_delete_event;
~~~