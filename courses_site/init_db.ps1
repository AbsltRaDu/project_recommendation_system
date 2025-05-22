# Параметры подключения
$port = 5432
$user = "postgres"
$targetDb = "courses_db"

# Создаём базу, если её нет (ошибки при существовании игнорируем)
psql -U $user -p $port -d postgres -c "CREATE DATABASE $targetDb;" 2>$null

# Выполняем основной скрипт в нужной базе
psql -U $user -p $port -d $targetDb -f "for_start_app.sql"
