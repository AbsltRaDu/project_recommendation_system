import numpy as np
from scipy.sparse import csr_matrix
import pickle
from app import Users

with open('lightfm_model.pkl', 'rb') as f:
    data = pickle.load(f)

model = data["model"]
dataset = data["dataset"]
user_features_matrix = data["user_features_matrix"]
item_features_matrix = data["item_features_matrix"]
items = data["items"]

list_users = []
max_id = db.session.query(db.func.max(Users.id)).scalar()  # Получаем максимальный ID

current_user_id = 1  # Начинаем с первого ID
while current_user_id <= max_id:
    user = Users.query.filter_by(id=current_user_id).first()  # Ищем одного пользователя
    if user:  # Если пользователь существует
        list_users.append(user)
    current_user_id += 1


mapping = dataset.mapping()              # получаем все отображения: users, items, features и т.д.
user_feature_map = mapping[1]            # берем отображение признаков пользователей

recomendation = []
for new_profile in list_users:
    # 12. Преобразуем строковые признаки в числовые ID
    feature_ids = [user_feature_map[f] for f in new_profile]  # перевели признаки в индексы


    data = np.ones(len(feature_ids))                       # все веса по 1.0
    rows = np.zeros(len(feature_ids))                      # одна строка, значит row = 0
    cols = feature_ids                                     # признаки располагаются в этих колонках
    new_user_matrix = csr_matrix((data, (rows, cols)), shape=(1, user_features_matrix.shape[1]))

    # 14. Предсказание интереса ко всем предметам для нового пользователя
    n_items = item_features_matrix.shape[0]                # количество курсов
    scores = model.predict(                                # получаем предсказания по dot product
        user_ids=0,                                        # т.к. new_user_matrix имеет одну строку — индекс 0
        item_ids=np.arange(n_items),
        user_features=new_user_matrix,
        item_features=item_features_matrix
    )

    # 15. Сортируем и выбираем топ-N рекомендаций
    # np.argsort возвращает индексы по убыванию значений
    recommended_indices = np.argsort(-scores)[:6]          # берём топ-6 курсов
    recomendation.append(recommended_indices)
    # Далее переходим в app, куда мы передали курсы в Recommends в формате <id|id_user|id_post>
