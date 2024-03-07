
// transform line breaks to <br> tags
export const nl2br = (str) => {
    return str.split('\n').map((item, key) => {
        return <span key={key}>{item}<br /></span>
    })
}

export const getJokometianTraitMapper = (t) => {
    const TRAITS_MAPPER = {
        'RACE': {
            'trait': t('jokometian.trait_incandescent'),
            'emoji': '🔥',
            'name': t('jokometian.name_incandescent'),
        },
        'RELIGION': {
            'trait': t('jokometian.trait_spiritual'),
            'emoji': '🕍',
            'name': t('jokometian.name_spiritual'),
        },
        'ETHNICITY': {
            'trait': t('jokometian.trait_diversity'),
            'emoji': '🌍',
            'name': t('jokometian.name_diversity'),
        },
        'GENDER': {
            'trait': t('jokometian.trait_wise'),
            'emoji': '👴',
            'name': t('jokometian.name_wise'),
        },
        'SEXUAL_ORIENTATION': {
            'trait': t('jokometian.trait_radiant'),
            'emoji': '🌈',
            'name': t('jokometian.name_radiant'),
        },
        'DISABILITY': {
            'trait': t('jokometian.trait_resilient'),
            'emoji': '🦿',
            'name': t('jokometian.name_resilient'),
        },
        'GENERIC_VIOLENCE': {
            'trait': t('jokometian.trait_fierce'),
            'emoji': '🗡️',
            'name': t('jokometian.name_fierce'),
        },
        'NO_OFFENSE_FOUND': {
            'trait': t('jokometian.trait_pure_soul'),
            'emoji': '😇',
            'name': t('jokometian.name_pure_soul'),
        },        
    };    
    return TRAITS_MAPPER;
}
