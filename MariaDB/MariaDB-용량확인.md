# MariaDB - Volume Check

* 리눅스 서버 콘솔에서 확인

  - DB별 용량 확인
  ~~~sh
  $ du -h /var/lib/mysql
  ~~~

  - 전체 용량 확인 
  ~~~sh
  $ du -sh /var/lib/mysql 
  ~~~ 

 

* mysql 또는 Workbench에서 확인

   - DB별 용량 확인
    ~~~sql
    SELECT table_schema "Database", ROUND(SUM(data_length+index_length)/1024/1024,1) "MB" FROM information_schema.TABLES GROUP BY 1;
    ~~~

      

    - 전체 용량 확인
    ~~~sql
    SELECT SUM(data_length+index_length)/1024/1024 used_MB, SUM(data_free)/1024/1024 free_MB FROM information_schema.tables;
    ~~~

    - 테이블 레코드 수가 많은 순으로 확인
    ~~~sql
    SELECT * FROM information_schema. tables WHERE TABLE_SCHEMA='DB명' ORDER BY TABLE_ROWS DESC
    ~~~



 
