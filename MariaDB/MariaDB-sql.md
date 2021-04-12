# Mysql - query
### SELECT (날짜별 FORMAT GROUP BY)
~~~sql
SELECT DATE_FORMAT(REG_DATE_TIME, '%yy-%mm-%dd') formatday, count(*) 
FROM USER 
WHERE USER = 'jdy'
AND REG_DATE_TIME >= '2021-01-15 00:00'
AND REG_DATE_TIME < '2021-02-19 00:00'
GROUP BY coltday;
~~~
</br>
</br>

### INSERT (select후 insert)
~~~sql
INSERT INTO MY_BOOK(PK_ID, `TYPE`, `NAME`, GUBUN)
SELECT   INFO.INFO_PK_ID, 'N', INFO.NAME, INFO.GUBUN 
FROM     BOOK_TYPE BOOK
         INNER JOIN BOOK_INFO INFO ON BOOK.ID = INFO.INFO_PK_ID
WHERE    BOOK.GUBUN = '001'
~~~

</br>
</br>

### UPDATE (연관테이블 없는값 select후 update)
~~~sql
UPDATE PRODUCT_ITEM as prd , 
	 (SELECT DISTINCT (INFO.INFO_VAL) AS PRD_NAME, PRD.ID AS PRD_ID  
	  FROM PRODUCT_ITEM PRD
			INNER JOIN PRODUCT_ITEM_INFO INFO 
			ON PRD.ID  = INFO.PRD_ID 
	  WHERE PRD.USER_NAME = 'jdy'
	  AND PRD.NAME = ''
	  GROUP BY PRD.ID 
	 ) as item
SET prd.PRD_NAME = item.NAME
WHERE prd.USER_NAME = 'jdy'
AND prd.ID = item.PRD_ID;
~~~

</br>
</br>

### DELETE (같은 테이블에서 중복된값 제거 )
~~~sql
DELETE rnk
FROM MY_PAGE_USER rnk
JOIN (
		SELECT   USER.ID
		FROM     MY_PAGE_USER USER
		WHERE    USER.NAME = 'jdy'
		HAVING COUNT(USER.DATA) > 1 
	 ) rr ON rr.ID = rnk.ID ;
~~~
