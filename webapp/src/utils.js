import moment from "moment";

moment.locale('pl');

export function fmtTimestamp(timestamp) {
    if (timestamp) {
        return moment(timestamp).format('LLLL');
    }
}
