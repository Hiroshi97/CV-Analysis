def word_filter(dictObject):
    new_counts = dict()
    for(key, value) in dictObject.items():
        if value >= 5:
            new_counts[key] = value

    return new_counts

def word_frequency(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def word_metric(word_count):
    if 450 <= word_count <= 650:
        metric_result = "Appropriate word count"
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Congrats! your resume has " + \
            str(word_count) + " words."
    else:
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Unfortunately, your resume has " + \
            str(word_count) + " words."
        if word_count <= 449:
            metric_result = "Add more words!"
        if word_count >= 650:
            metric_result = "Reduce amount of words!"

    return metric_result + word_count_warning

