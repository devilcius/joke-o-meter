
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
        },
        'RELIGION': {
            'trait': t('jokometian.trait_spiritual'),
            'emoji': '🕍',
        },
        'ETHNICITY': {
            'trait': t('jokometian.trait_diversity'),
            'emoji': '🌍',
        },
        'GENDER': {
            'trait': t('jokometian.trait_wise'),
            'emoji': '👴',
        },
        'SEXUAL_ORIENTATION': {
            'trait': t('jokometian.trait_radiant'),
            'emoji': '🌈',
        },
        'DISABILITY': {
            'trait': t('jokometian.trait_resilient'),
            'emoji': '🦿',
            'name': t('jokometian.name_resilient'),
        },
        'GENERIC_VIOLENCE': {
            'trait': t('jokometian.trait_fierce'),
            'emoji': '🗡️',
        },
        'NO_OFFENSE_FOUND': {
            'trait': t('jokometian.trait_pure_soul'),
            'emoji': '😇',
        },
        'GRUMPY': {
            'trait': t('jokometian.trait_grumpy'),
            'emoji': '😡',
        },
        'GIGGLY': {
            'trait': t('jokometian.trait_giggly'),
            'emoji': '😂',
        }, 
        'DIABOLICAL': {
            'trait': t('jokometian.trait_diabolical'),
            'emoji': '😈',
        },
    };    
    return TRAITS_MAPPER;
}
