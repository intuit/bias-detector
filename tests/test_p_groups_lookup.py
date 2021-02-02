from bias_detector.p_groups_lookup import p_gender_given_first_name_df, p_first_name_given_race_df


def test_first_names_p_gender_df():
    assert p_gender_given_first_name_df.at['DAVID', 'male'] == 0.9974672857745884


def test_p_first_name_given_race_df():
    assert p_first_name_given_race_df.at['DAVID', 'white'] == 0.020446108002980624
