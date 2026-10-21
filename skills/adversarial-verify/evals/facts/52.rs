// prompt-sha256: 8bd1806145649493a8301ab5dc02c59a2fb13ceb153a15424bb28028a628a105
// Eval 52: the test asserting 29 days in February 2024 fails on the function as shown.
fn days_in_month(year: u32, month: u32) -> u32 {
    let _ = year;
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => 28,
        _ => panic!("bad month"),
    }
}

fn main() {
    assert_eq!(days_in_month(2024, 2), 28); // so assert_eq!(.., 29) fails: left 28, right 29
    assert_ne!(days_in_month(2024, 2), 29);
    assert_eq!(days_in_month(2026, 4), 30);
    assert_eq!(days_in_month(2026, 1), 31);
    println!("ok 52");
}
