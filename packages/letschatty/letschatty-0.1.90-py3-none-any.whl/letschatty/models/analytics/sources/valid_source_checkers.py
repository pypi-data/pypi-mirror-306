from ...utils.types.source_types import SourceType, SourceCheckerType

SOURCE_CHECKER_MAPPING = {
    SourceType.OTHER_SOURCE: [SourceCheckerType.SIMILARITY, SourceCheckerType.LITERAL, SourceCheckerType.SMART_MESSAGES],
    SourceType.PURE_AD: [SourceCheckerType.REFERRAL],
    SourceType.WHATSAPP_DEFAULT_SOURCE: [SourceCheckerType.FIRST_CONTACT],
    SourceType.TOPIC_DEFAULT_SOURCE: [SourceCheckerType.SMART_MESSAGES],
    SourceType.UTM_SOURCE: [SourceCheckerType.SMART_MESSAGES]
}

def is_valid_source_checker(source_type: SourceType, source_checker: SourceCheckerType) -> bool:
    return source_checker in SOURCE_CHECKER_MAPPING[source_type]
