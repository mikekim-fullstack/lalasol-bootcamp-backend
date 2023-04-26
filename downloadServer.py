import os
# When execute railway up, automatically local media folder uploaded.
# So in order to prevent it, first download media folder from server
# and unzip it and update all files in local media folder.
# Meanwhile also Postgres DB should be backuped in local folder.
# Then execute railway up


#PGPASSWORD= IrcceCzUiMLjxTWg29Yi
download_media = 'curl https://lalasol-bootcamp-backend-production.up.railway.app/api/download/ --output media.zip'
update_media = 'unzip -o media.zip -d media'
backup_db ='pg_dump -h containers-us-west-25.railway.app  -d railway -U postgres -p 6144 -W -F t > lalasol-postgres-db.dump'
# railway_up = 'railway up'
# os.system(backup_db+'; ' +download_media + ' && ' +update_media + ' && ' + railway_up)
os.system(backup_db+'; ' +download_media + ' && ' +update_media )
