@echo off

FOR /F "tokens=*" %%i IN ('docker compose ps -aq "mongo"') DO SET MONGO=%%i
SET COMMAND=db.users.updateOne({account: "%1"}, {$set: {status: 1}})

docker exec %MONGO% mongosh localhost/Micala -u root -p root --authenticationDatabase admin --eval %COMMAND%
