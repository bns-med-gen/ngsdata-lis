from typing import Optional
from sqlalchemy import ForeignKey, Index, Integer, REAL, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Biomaterial(Base):
    __tablename__ = 'biomaterial'
    __table_args__ = (
        Index('idx_biomaterial_biomaterCode', 'biomaterCode'),
    )

    biomaterId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    biomaterCode: Mapped[Optional[str]] = mapped_column(Text)
    patientId: Mapped[Optional[str]] = mapped_column(Text)
    isDeleted: Mapped[Optional[int]] = mapped_column(Integer)
    ВидМатериала: Mapped[Optional[str]] = mapped_column(Text)
    ДатаФактическогоПолучения: Mapped[Optional[str]] = mapped_column(Text)
    ВариантПолученияМатериала: Mapped[Optional[str]] = mapped_column(Text)
    Штрихкод: Mapped[Optional[str]] = mapped_column(Text)
    СтатусМатериала: Mapped[Optional[str]] = mapped_column(Text)
    history: Mapped[Optional[str]] = mapped_column(Text)


class LisDictionaryItems(Base):
    __tablename__ = 'lis_dictionary_items'

    price_item_code: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    price_item_name: Mapped[Optional[str]] = mapped_column(Text)
    test_type: Mapped[Optional[str]] = mapped_column(Text)


class LisParams(Base):
    __tablename__ = 'lis_params'

    category: Mapped[Optional[str]] = mapped_column(Text, primary_key=True, nullable=True)
    value: Mapped[Optional[str]] = mapped_column(Text, primary_key=True, nullable=True)


class LisProtocols(Base):
    __tablename__ = 'lis_protocols'

    extraction_protocol_name: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    extraction_protocol_createdate: Mapped[Optional[str]] = mapped_column(Text)
    extraction_operator: Mapped[Optional[str]] = mapped_column(Text)
    extraction_kit: Mapped[Optional[str]] = mapped_column(Text)
    extraction_instrument: Mapped[Optional[str]] = mapped_column(Text)
    extraction_elution: Mapped[Optional[str]] = mapped_column(Text)
    extraction_elution_volume: Mapped[Optional[float]] = mapped_column(REAL)
    extraction_protocol_stage: Mapped[Optional[str]] = mapped_column(Text)
    extraction_protocol_closedate: Mapped[Optional[str]] = mapped_column(Text)

    lis_protocol_samples: Mapped[list['LisProtocolSamples']] = relationship('LisProtocolSamples', back_populates='lis_protocols')


class LisSampleMetadata(Base):
    __tablename__ = 'lis_sample_metadata'
    __table_args__ = (
        Index('idx_lis_sample_metadata_biomater_id', 'biomater_id'),
        Index('idx_lis_sample_metadata_lab_sample_id', 'lab_sample_id'),
        Index('idx_lis_sample_metadata_medical_test_id', 'medical_test_id')
    )

    lab_sample_id: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    medical_test_id: Mapped[Optional[str]] = mapped_column(Text)
    biomater_id: Mapped[Optional[str]] = mapped_column(Text)
    patient_id: Mapped[Optional[str]] = mapped_column(Text)
    dna_ids: Mapped[Optional[str]] = mapped_column(Text)
    lab_sample_stage: Mapped[Optional[str]] = mapped_column(Text)
    lab_sample_comment: Mapped[Optional[str]] = mapped_column(Text)

    lis_protocol_samples: Mapped[list['LisProtocolSamples']] = relationship('LisProtocolSamples', back_populates='lab_sample')


class LisSettings(Base):
    __tablename__ = 'lis_settings'

    key: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    value: Mapped[Optional[str]] = mapped_column(Text)


class LisTechprocesses(Base):
    __tablename__ = 'lis_techprocesses'

    test_type: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    is_extraction: Mapped[Optional[int]] = mapped_column(Integer)
    test_type_prefix: Mapped[Optional[str]] = mapped_column(Text)


class MedicalFiles(Base):
    __tablename__ = 'medical_files'

    medicalFileId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    НомерКарты: Mapped[Optional[str]] = mapped_column(Text)
    ДиагнозПриОбращении: Mapped[Optional[str]] = mapped_column(Text)
    ВходящийДиагнозНеизвестен: Mapped[Optional[int]] = mapped_column(Integer)
    Примечание: Mapped[Optional[str]] = mapped_column(Text)


class MedicalReports(Base):
    __tablename__ = 'medical_reports'

    medicalReportId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    medicalTestId: Mapped[Optional[str]] = mapped_column(Text)
    Исполнитель: Mapped[Optional[str]] = mapped_column(Text)
    Проведен: Mapped[Optional[int]] = mapped_column(Integer)
    isDeleted: Mapped[Optional[int]] = mapped_column(Integer)
    Номер: Mapped[Optional[str]] = mapped_column(Text)
    Дата: Mapped[Optional[str]] = mapped_column(Text)
    МатериалНеПригоден: Mapped[Optional[int]] = mapped_column(Integer)
    ДатаОтправкиЗаключения: Mapped[Optional[str]] = mapped_column(Text)
    СтатусДиагноза: Mapped[Optional[str]] = mapped_column(Text)
    МКБ10Код: Mapped[Optional[str]] = mapped_column(Text)
    ДиагнозНаименование: Mapped[Optional[str]] = mapped_column(Text)
    РезультатИсследования: Mapped[Optional[str]] = mapped_column(Text)
    ЗаключениеОтправленоПоПочте: Mapped[Optional[int]] = mapped_column(Integer)


class MedicalTests(Base):
    __tablename__ = 'medical_tests'
    __table_args__ = (
        Index('idx_medical_tests_preyskurant', 'ПунктПрейскуранта'),
    )

    medicalTestId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    medicalTestCode: Mapped[Optional[str]] = mapped_column(Text)
    ПунктПрейскуранта: Mapped[Optional[str]] = mapped_column(Text)
    НазваниеПункта: Mapped[Optional[str]] = mapped_column(Text)
    НаправилНаИсследование: Mapped[Optional[str]] = mapped_column(Text)
    ДатаНаправления: Mapped[Optional[str]] = mapped_column(Text)
    ДатаОплаты: Mapped[Optional[str]] = mapped_column(Text)
    ПлановаяДатаГотовностиДляЛаборатории: Mapped[Optional[str]] = mapped_column(Text)
    НаправляющийДиагноз: Mapped[Optional[str]] = mapped_column(Text)
    ДатаПринятияВРаботу: Mapped[Optional[str]] = mapped_column(Text)
    ПринятоВРаботу: Mapped[Optional[int]] = mapped_column(Integer)
    Примечание: Mapped[Optional[str]] = mapped_column(Text)
    ТипОплаты: Mapped[Optional[str]] = mapped_column(Text)
    СостояниеЗдоровьяНаМоментИсследования: Mapped[Optional[str]] = mapped_column(Text)
    ФормаИсследования: Mapped[Optional[str]] = mapped_column(Text)
    ПорядокИсследования: Mapped[Optional[str]] = mapped_column(Text)
    МедицинскаяОрганизацияКраткоеНаименование: Mapped[Optional[str]] = mapped_column(Text)
    МедицинскаяОрганизацияРегионНаименование: Mapped[Optional[str]] = mapped_column(Text)
    isDeleted: Mapped[Optional[int]] = mapped_column(Integer)
    samples: Mapped[Optional[str]] = mapped_column(Text)


class Patients(Base):
    __tablename__ = 'patients'
    __table_args__ = (
        Index('idx_patients_medicalFileID', 'medicalFileID'),
    )

    patientID: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)
    patientCode: Mapped[Optional[str]] = mapped_column(Text)
    Пол: Mapped[Optional[str]] = mapped_column(Text)
    ДатаРождения: Mapped[Optional[str]] = mapped_column(Text)
    Регион: Mapped[Optional[str]] = mapped_column(Text)
    ОтношениеКОбратившемуся: Mapped[Optional[str]] = mapped_column(Text)
    СогласиеБТК: Mapped[Optional[int]] = mapped_column(Integer)
    НомерКарты: Mapped[Optional[str]] = mapped_column(Text)
    medicalFileID: Mapped[Optional[str]] = mapped_column(Text)


class TestSamples(Base):
    __tablename__ = 'test_samples'
    __table_args__ = (
        Index('idx_test_samples_biomaterId', 'biomaterId'),
        Index('idx_test_samples_patientId', 'patientId')
    )

    medicalTestId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True, nullable=True)
    biomaterId: Mapped[Optional[str]] = mapped_column(Text, primary_key=True, nullable=True)
    patientId: Mapped[Optional[str]] = mapped_column(Text)


class LisProtocolSamples(Base):
    __tablename__ = 'lis_protocol_samples'

    extraction_protocol_name: Mapped[Optional[str]] = mapped_column(ForeignKey('lis_protocols.extraction_protocol_name'), primary_key=True, nullable=True)
    lab_sample_id: Mapped[Optional[str]] = mapped_column(ForeignKey('lis_sample_metadata.lab_sample_id'), primary_key=True, nullable=True)
    extraction_protocol_position: Mapped[Optional[int]] = mapped_column(Integer)
    dna_id: Mapped[Optional[str]] = mapped_column(Text)
    extraction_dna_purity: Mapped[Optional[float]] = mapped_column(REAL)
    extraction_dna_concentration: Mapped[Optional[float]] = mapped_column(REAL)
    extraction_dna_volume: Mapped[Optional[float]] = mapped_column(REAL)
    extraction_dna_comment: Mapped[Optional[str]] = mapped_column(Text)
    extraction_dna_status: Mapped[Optional[str]] = mapped_column(Text)

    lis_protocols: Mapped[Optional['LisProtocols']] = relationship('LisProtocols', back_populates='lis_protocol_samples')
    lab_sample: Mapped[Optional['LisSampleMetadata']] = relationship('LisSampleMetadata', back_populates='lis_protocol_samples')
