from hundred.classes import Configuration
from hundred.script import ScriptSection, data


class IntroductionStateTopicSection(ScriptSection):
    def get_content(self) -> str:
        return self.config.name.capitalize() + '.'


class SummarizedTopicSection(ScriptSection):
    def get_content(self) -> str:
        wikidata_data = data.make_request_json(
            f'https://en.wikipedia.org/api/rest_v1/page/summary/{self.config.wikipedia}')

        extract = wikidata_data['extract']
        what_is_it_keyword = 'is a'
        what_is_it_index = extract.lower().index(what_is_it_keyword) + len(what_is_it_keyword)
        summary = extract[what_is_it_index:]

        if 'aeiou' in extract[1].lower():
            summary = 'An' + summary
        else:
            summary = 'A' + summary

        period = summary.index('.')

        if ',' in summary:
            comma = summary.index(',')
            stop_point = min(comma, period)
        else:
            stop_point = period

        return summary[:stop_point] + '.'


class CreatedByInTopicSection(ScriptSection):
    def get_content(self) -> str:
        return 'It was created in [year] by [title of person] [person].'


class WhereIsTopicUsedSection(ScriptSection):
    def get_content(self) -> str:
        return 'Today, it is used in [applications].'


def get_default_sections(config: Configuration):
    # [
    #     [(section), (fallback section), (fallback_section)...],
    #     [(section), (fallback section), (fallback_section)...],
    #     [(section), (fallback section), (fallback_section)...],
    # ]

    return [
        [IntroductionStateTopicSection(config)],
        [SummarizedTopicSection(config)],
        [CreatedByInTopicSection(config)],
        [WhereIsTopicUsedSection(config)]
    ]