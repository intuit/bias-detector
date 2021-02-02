from bias_detector.EmailFullNameExtractor import EmailFullNameExtractor

extractor = EmailFullNameExtractor()


class TestEmailFullNameExtractor:

    def test_get_email_full_name(self):
        # full_name = extractor.get_email_full_name('robobsad@gmail.com')
        # assert full_name.first_name == 'rob'
        # full_name = extractor.get_email_full_name('lisapzdafd.245@gmail.com')
        # assert full_name.first_name == 'lisa'
        # full_name = extractor.get_email_full_name('adammartinezjr73@gmail.com')
        # assert full_name.first_name == 'adam' and full_name.last_name == 'martinez'
        full_name = extractor.get_email_full_name('sarahk42@gmail.com')
        assert full_name.first_name == 'sarah'
        full_name = extractor.get_email_full_name('moshe.cohen@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.get_email_full_name('cohen.moshe@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.get_email_full_name('cohenmoshe@gmail.com')
        assert full_name.first_name == 'moshe' and full_name.last_name == 'cohen'
        full_name = extractor.get_email_full_name('moshe@gmail.com')
        assert full_name.first_name == 'moshe'
        full_name = extractor.get_email_full_name('cohen@gmail.com')
        assert full_name.last_name == 'cohen'
        full_name = extractor.get_email_full_name('mcohen@gmail.com')
        assert full_name.last_name == 'cohen'
        full_name = extractor.get_email_full_name('rbrownlr@gmail.com')
        assert full_name.first_name == ''
        full_name = extractor.get_email_full_name('ray_smith@gmail.com')
        assert full_name.first_name == 'ray'
        full_name = extractor.get_email_full_name('rbrownlr@gmail.com')
        assert full_name.last_name == ''
        # full_name = extractor.get_email_full_name('wlvksddavis@gmail.com')
        # assert full_name.last_name == 'davis'
