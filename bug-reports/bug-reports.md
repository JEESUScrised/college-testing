# Баг-репорты — КТ 04

Все дефекты — **учебные seeded-баги** Campus Portal Demo.  
Трекер: GitHub Issues репозитория [JEESUScrised/college-testing](https://github.com/JEESUScrised/college-testing).

---

## BUG-KT04-001 (SEED-001)

| Поле | Значение |
|---|---|
| Bug ID | BUG-KT04-001 |
| Issue | https://github.com/JEESUScrised/college-testing/issues/1 |
| Summary | Вход принимает пустой пароль |
| Description | При непустом логине и пустом пароле приложение открывает личный кабинет вместо ошибки авторизации. |
| Steps | 1) Открыть `index.html` 2) Логин `student` 3) Пароль пустой 4) Войти |
| Expected | Остаться на странице входа, показать ошибку |
| Actual | Открыт dashboard «Личный кабинет», user=`student` |
| Severity | Major |
| Priority | High |
| Environment | Windows 11, Chrome 154.0.8037.98, Selenium 4.50.0 |
| Evidence | `screenshots/kt04/tc02_seed001_empty_password.png`; тест TC-02 FAIL |
| Reproducibility | Always |
| Status | **Open** |

---

## BUG-KT04-002 (SEED-002)

| Поле | Значение |
|---|---|
| Bug ID | BUG-KT04-002 |
| Issue | https://github.com/JEESUScrised/college-testing/issues/2 |
| Summary | Регистрация принимает email без TLD |
| Description | Email `user@mail` проходит валидацию; отображается успех регистрации. |
| Steps | 1) `register.html` 2) Имя Иван, email `user@mail`, пароль любой 3) Зарегистрироваться |
| Expected | Ошибка «Некорректный email» |
| Actual | «Регистрация успешна» |
| Severity | Major |
| Priority | High |
| Environment | Windows 11, Chrome 154.0.8037.98, Selenium 4.50.0 |
| Evidence | `screenshots/kt04/tc03_seed002_invalid_email.png`; тест TC-03 FAIL |
| Reproducibility | Always |
| Status | **Open** |

---

## BUG-KT04-003 (SEED-003)

| Поле | Значение |
|---|---|
| Bug ID | BUG-KT04-003 |
| Issue | https://github.com/JEESUScrised/college-testing/issues/3 |
| Summary | Заказ принимается с количеством 0 |
| Description | Форма заказа считает quantity=0 допустимым и показывает успех. |
| Steps | 1) Войти student/student123 2) Количество 0 3) Оформить заказ |
| Expected | Ошибка «Количество должно быть больше 0» |
| Actual | «Заказ оформлен успешно (шт.: 0)» |
| Severity | Minor |
| Priority | Medium |
| Environment | Windows 11, Chrome 154.0.8037.98, Selenium 4.50.0 |
| Evidence | `screenshots/kt04/tc04_seed003_zero_quantity.png`; тест TC-04 FAIL |
| Reproducibility | Always |
| Status | **Open** |
