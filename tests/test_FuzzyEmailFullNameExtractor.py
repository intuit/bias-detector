from bias_detector.fuzzy_names_from_emails.FuzzyEmailFullNameExtractor import FuzzyEmailFullNameExtractor

extractor = FuzzyEmailFullNameExtractor()


class TestFuzzyEmailFullNameExtractor:

    def test_fuzzily_get_email_full_name(self):
        full_name = extractor.fuzzily_get_email_full_name('sarahk42@gmail.com')
        assert full_name.first_name == 'sarah'
        full_name = extractor.fuzzily_get_email_full_name('moshe.cohen@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.fuzzily_get_email_full_name('cohen.moshe@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.fuzzily_get_email_full_name('cohenmoshe@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.fuzzily_get_email_full_name('moshe@gmail.com')
        assert full_name.first_name == 'moshe'
        full_name = extractor.fuzzily_get_email_full_name('cohen@gmail.com')
        assert full_name.last_name == 'cohen'
        full_name = extractor.fuzzily_get_email_full_name('mcohen@gmail.com')
        assert full_name.last_name == 'cohen'
        full_name = extractor.fuzzily_get_email_full_name('rbrownlr@gmail.com')
        assert full_name.first_name == ''
        full_name = extractor.fuzzily_get_email_full_name('ray_smith@gmail.com')
        assert full_name.first_name == 'ray'
        full_name = extractor.fuzzily_get_email_full_name('rbrownlr@gmail.com')
        assert full_name.last_name == ''
