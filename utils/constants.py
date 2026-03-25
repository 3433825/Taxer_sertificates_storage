class CertConstants:
    # Очікувані імена власників (Common Name)
    VALID_OWNER = "Олег Андрійович (Тест)"
    EXPIRED_OWNER = "Таксер Тест Тестерович"
    LONG_NAME_OWNER = "Володимир Борисович (Тест)"

    # Назви полів у деталях (Вимога 7)
    EXPECTED_FIELD_COMMON_NAME = "Common Name"
    EXPECTED_FIELD_ISSUER = "Issuer CN"

    FIELD_VALID_FROM = "Valid From"
    FIELD_VALID_TO = "Valid To"
    ACTUAL_FIELD_SUBJECT_CN = "SubjectCN"
    ACTUAL_FIELD_ISSUER_CN = "IssuerCN"
    ACTUAL_FIELD_VALID_FROM = "ValidFrom"
    ACTUAL_FIELD_VALID_TILL = "ValidTill"

    EMPTY_STATE_MESSAGE = "Нема жодного сертифікату"
