from rest_framework import serializers


class BiomaterialSerializer(serializers.Serializer):
    """Serializer for Biomaterial (read-only)"""
    biomaterId = serializers.CharField()
    biomaterCode = serializers.CharField(required=False, allow_null=True)
    patientId = serializers.CharField(required=False, allow_null=True)
    isDeleted = serializers.IntegerField(required=False, allow_null=True)
    ВидМатериала = serializers.CharField(required=False, allow_null=True)
    ДатаФактическогоПолучения = serializers.CharField(required=False, allow_null=True)
    ВариантПолученияМатериала = serializers.CharField(required=False, allow_null=True)
    Штрихкод = serializers.CharField(required=False, allow_null=True)
    СтатусМатериала = serializers.CharField(required=False, allow_null=True)
    history = serializers.CharField(required=False, allow_null=True)


class MedicalFilesSerializer(serializers.Serializer):
    """Serializer for MedicalFiles (read-only)"""
    medicalFileId = serializers.CharField()
    НомерКарты = serializers.CharField(required=False, allow_null=True)
    ДиагнозПриОбращении = serializers.CharField(required=False, allow_null=True)
    ВходящийДиагнозНеизвестен = serializers.IntegerField(required=False, allow_null=True)
    Примечание = serializers.CharField(required=False, allow_null=True)


class MedicalReportsSerializer(serializers.Serializer):
    """Serializer for MedicalReports (read-only)"""
    medicalReportId = serializers.CharField()
    medicalTestId = serializers.CharField(required=False, allow_null=True)
    Исполнитель = serializers.CharField(required=False, allow_null=True)
    Проведен = serializers.IntegerField(required=False, allow_null=True)
    isDeleted = serializers.IntegerField(required=False, allow_null=True)
    Номер = serializers.CharField(required=False, allow_null=True)
    Дата = serializers.CharField(required=False, allow_null=True)
    МатериалНеПригоден = serializers.IntegerField(required=False, allow_null=True)
    ДатаОтправкиЗаключения = serializers.CharField(required=False, allow_null=True)
    СтатусДиагноза = serializers.CharField(required=False, allow_null=True)
    МКБ10Код = serializers.CharField(required=False, allow_null=True)
    ДиагнозНаименование = serializers.CharField(required=False, allow_null=True)
    РезультатИсследования = serializers.CharField(required=False, allow_null=True)
    ЗаключениеОтправленоПоПочте = serializers.IntegerField(required=False, allow_null=True)


class MedicalTestsSerializer(serializers.Serializer):
    """Serializer for MedicalTests (read-only)"""
    medicalTestId = serializers.CharField()
    medicalTestCode = serializers.CharField(required=False, allow_null=True)
    ПунктПрейскуранта = serializers.CharField(required=False, allow_null=True)
    НазваниеПункта = serializers.CharField(required=False, allow_null=True)
    НаправилНаИсследование = serializers.CharField(required=False, allow_null=True)
    ДатаНаправления = serializers.CharField(required=False, allow_null=True)
    ДатаОплаты = serializers.CharField(required=False, allow_null=True)
    ПлановаяДатаГотовностиДляЛаборатории = serializers.CharField(required=False, allow_null=True)
    НаправляющийДиагноз = serializers.CharField(required=False, allow_null=True)
    ДатаПринятияВРаботу = serializers.CharField(required=False, allow_null=True)
    ПринятоВРаботу = serializers.IntegerField(required=False, allow_null=True)
    Примечание = serializers.CharField(required=False, allow_null=True)
    ТипОплаты = serializers.CharField(required=False, allow_null=True)
    СостояниеЗдоровьяНаМоментИсследования = serializers.CharField(required=False, allow_null=True)
    ФормаИсследования = serializers.CharField(required=False, allow_null=True)
    ПорядокИсследования = serializers.CharField(required=False, allow_null=True)
    МедицинскаяОрганизацияКраткоеНаименование = serializers.CharField(required=False, allow_null=True)
    МедицинскаяОрганизацияРегионНаименование = serializers.CharField(required=False, allow_null=True)
    isDeleted = serializers.IntegerField(required=False, allow_null=True)
    samples = serializers.CharField(required=False, allow_null=True)


class PatientsSerializer(serializers.Serializer):
    """Serializer for Patients (read-only)"""
    patientID = serializers.CharField()
    patientCode = serializers.CharField(required=False, allow_null=True)
    Пол = serializers.CharField(required=False, allow_null=True)
    ДатаРождения = serializers.CharField(required=False, allow_null=True)
    Регион = serializers.CharField(required=False, allow_null=True)
    ОтношениеКОбратившемуся = serializers.CharField(required=False, allow_null=True)
    СогласиеБТК = serializers.IntegerField(required=False, allow_null=True)
    НомерКарты = serializers.CharField(required=False, allow_null=True)
    medicalFileID = serializers.CharField(required=False, allow_null=True)


class TestSamplesSerializer(serializers.Serializer):
    """Serializer for TestSamples (read-only)"""
    medicalTestId = serializers.CharField(required=False, allow_null=True)
    biomaterId = serializers.CharField(required=False, allow_null=True)
    patientId = serializers.CharField(required=False, allow_null=True)

