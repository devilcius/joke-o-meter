// transform line breaks to <br> tags
export const nl2br = (str) => {
    return str.split('\n').map((item, key) => {
        return <span key={key}>{item}<br /></span>
    })
}