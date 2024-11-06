//! **spellcraft** is a utility or "helper" library primarily designed
//! for use in the [dataclass-wizard] library, facilitating
//! various case conversions.
//!
//! This library aims to be Unicode-aware, internally consistent,
//! and reasonably performant, providing convenient case conversion
//! between common naming conventions.
//!
//! ### Supported Cases:
//!
//! 1. UpperCamelCase
//! 2. lowerCamelCase
//! 3. snake_case
//! 4. kebab-case
//! 5. SHOUTY_SNAKE_CASE
//! 6. Title Case
//! 7. SHOUTY-KEBAB-CASE
//! 8. Train-Case
//!
//! [dataclass-wizard]: https://dataclass-wizard.readthedocs.io/
//!
#![deny(missing_docs)]
#![forbid(unsafe_code)]

extern crate alloc;

#[path = "kebab.rs"]
mod kebab_mod;
#[path = "lower_camel.rs"]
mod lower_camel_mod;
#[path = "shouty_kebab.rs"]
mod shouty_kebab_mod;
#[path = "shouty_snake.rs"]
mod shouty_snake_mod;
#[path = "snake.rs"]
mod snake_mod;
#[path = "title.rs"]
mod title_mod;
#[path = "train.rs"]
mod train_mod;
#[path = "upper_camel.rs"]
mod upper_camel_mod;

pub use kebab_mod::{AsKebabCase, ToKebabCase};
pub use lower_camel_mod::{AsLowerCamelCase, ToLowerCamelCase};
pub use shouty_kebab_mod::{AsShoutyKebabCase, ToShoutyKebabCase};
pub use shouty_snake_mod::{
    AsShoutySnakeCase, AsShoutySnakeCase as AsShoutySnekCase, ToShoutySnakeCase, ToShoutySnekCase,
};
pub use snake_mod::{AsSnakeCase, AsSnakeCase as AsSnekCase, ToSnakeCase, ToSnekCase};
pub use title_mod::{AsTitleCase, ToTitleCase};
pub use train_mod::{AsTrainCase, ToTrainCase};
pub use upper_camel_mod::{
    AsUpperCamelCase, AsUpperCamelCase as AsPascalCase, ToPascalCase, ToUpperCamelCase,
};

use core::fmt;

use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn spellcraft(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // m.add_function(wrap_pyfunction!(sum, m)?)?;
    m.add_function(wrap_pyfunction!(snake, m)?)?;
    // m.add_function(wrap_pyfunction!(snake_many, m)?)?;
    m.add_function(wrap_pyfunction!(lower_camel, m)?)?;
    // m.add_function(wrap_pyfunction!(lower_camel_many, m)?)?;
    m.add_function(wrap_pyfunction!(title, m)?)?;
    // m.add_function(wrap_pyfunction!(title_many, m)?)?;
    m.add_function(wrap_pyfunction!(upper_camel, m)?)?;
    // m.add_function(wrap_pyfunction!(upper_camel_many, m)?)?;
    m.add_function(wrap_pyfunction!(kebab, m)?)?;
    // m.add_function(wrap_pyfunction!(kebab_many, m)?)?;
    m.add_function(wrap_pyfunction!(shouty_kebab, m)?)?;
    // m.add_function(wrap_pyfunction!(shouty_kebab_many, m)?)?;
    m.add_function(wrap_pyfunction!(shouty_snake, m)?)?;
    // m.add_function(wrap_pyfunction!(shouty_snake_many, m)?)?;

    Ok(())
}

/// Finds the sum of two numbers.
// #[pyfunction]
// fn sum(a: i32, b: i32) -> PyResult<i32> {
//     Ok(a + b)
// }

/// Convert to snake_case.
///
/// In snake_case, word boundaries are indicated by underscores.
///
/// Example:
///     >>> from pyheck import snake
///     >>> snake("We carry a new world here, in our hearts.")
///     'we_carry_a_new_world_here_in_our_hearts'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn snake(s: &str) -> String {
    s.to_snake_case()
}

/// Convert a list of strings to snake_case.
///
/// In snake_case, word boundaries are indicated by underscores.
///
/// Example:
///     >>> from pyheck import snake_many
///     >>> snake_many(["DeviceType", "fooBar"])
///     ['device_type', 'foo_bar']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn snake_many(strings: Vec<&str>) -> Vec<String> {
//     strings.par_iter().map(|s| s.to_snake_case()).collect()
// }

/// Convert to lowerCamelCase.
///
/// In lowerCamelCase, word boundaries are indicated by capital letters,
/// excepting the first word.
///
/// Example:
///     >>> from pyheck import lower_camel
///     >>> lower_camel("It is we who built these palaces and cities.")
///     'itIsWeWhoBuiltThesePalacesAndCities'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn lower_camel(s: &str) -> String {
    s.to_lower_camel_case()
}

/// Convert a list of strings to lowerCamelCase.
///
/// In lowerCamelCase, word boundaries are indicated by capital letters,
/// excepting the first word.
///
/// Example:
///     >>> from pyheck import lower_camel_many
///     >>> lower_camel_many(["It is we", "who built these"])
///     ['itIsWe', 'whoBuiltThese']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn lower_camel_many(strings: Vec<&str>) -> Vec<String> {
//     strings
//         .par_iter()
//         .map(|s| s.to_lower_camel_case())
//         .collect()
// }

/// Convert to Title Case.
///
/// In Title Case, word boundaries are indicated by spaces, and every word is
/// capitalized.
///
/// Example:
///     >>> from pyheck import title
///     >>> title("We have always lived in slums and holes in the wall.")
///     'We Have Always Lived In Slums And Holes In The Wall'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn title(s: &str) -> String {
    s.to_title_case()
}

/// Convert a list of strings to Title Case.
///
/// In Title Case, word boundaries are indicated by spaces, and every word is
/// capitalized.
///
/// Example:
///     >>> from pyheck import title_many
///     >>> title_many(["We have always", "lived in slums"])
///     ['We Have Always', 'Lived In Slums']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn title_many(strings: Vec<&str>) -> Vec<String> {
//     strings.par_iter().map(|s| s.to_title_case()).collect()
// }

/// Convert to UpperCamelCase.
///
/// In UpperCamelCase, word boundaries are indicated by capital letters,
/// including the first word.
///
/// Example:
///     >>> from pyheck import upper_camel
///     >>> upper_camel("We are not in the least afraid of ruins.")
///     'WeAreNotInTheLeastAfraidOfRuins'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn upper_camel(s: &str) -> String {
    s.to_upper_camel_case()
}

/// Convert a list of strings to UpperCamelCase.
///
/// In UpperCamelCase, word boundaries are indicated by capital letters,
/// including the first word.
///
/// Example:
///     >>> from pyheck import upper_camel_many
///     >>> upper_camel_many(["We are not", "in the least"])
///     ['WeAreNot', 'InTheLeast']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn upper_camel_many(strings: Vec<&str>) -> Vec<String> {
//     strings
//         .par_iter()
//         .map(|s| s.to_upper_camel_case())
//         .collect()
// }

/// Convert to kebab-case.
///
/// In kebab-case, word boundaries are indicated by hyphens.
///
/// Example:
///     >>> from pyheck import kebab
///     >>> kebab("We are going to inherit the earth.")
///     'we-are-going-to-inherit-the-earth'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn kebab(s: &str) -> String {
    s.to_kebab_case()
}

/// Convert list of strings to kebab-case.
///
/// In kebab-case, word boundaries are indicated by hyphens.
///
/// Example:
///     >>> from pyheck import kebab_many
///     >>> kebab_many(["We are going", "to inherit the earth."])
///     ['we-are-going', 'to-inherit-the-earth']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn kebab_many(strings: Vec<&str>) -> Vec<String> {
//     strings.par_iter().map(|s| s.to_kebab_case()).collect()
// }

/// Convert to SHOUTY-KEBAB-CASE.
///
/// In SHOUTY-KEBAB-CASE, word boundaries are indicated by hyphens and all
/// words are in uppercase.
///
/// Example:
///     >>> from pyheck import shouty_kebab
///     >>> shouty_kebab("We are going to inherit the earth.")
///     'WE-ARE-GOING-TO-INHERIT-THE-EARTH'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn shouty_kebab(s: &str) -> String {
    s.to_shouty_kebab_case()
}

/// Convert a list of strings to SHOUTY-KEBAB-CASE.
///
/// In SHOUTY-KEBAB-CASE, word boundaries are indicated by hyphens and all
/// words are in uppercase.
///
/// Example:
///     >>> from pyheck import shouty_kebab_many
///     >>> shouty_kebab_many(["We are going", "to inherit the earth."])
///     ['WE-ARE-GOING', 'TO-INHERIT-THE-EARTH']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn shouty_kebab_many(strings: Vec<&str>) -> Vec<String> {
//     strings
//         .par_iter()
//         .map(|s| s.to_shouty_kebab_case())
//         .collect()
// }

/// Convert to SHOUTY_SNAKE_CASE.
///
/// In SHOUTY_SNAKE_CASE, word boundaries are indicated by underscores and all
/// words are in uppercase.
///
/// Example:
///     >>> from pyheck import shouty_snake
///     >>> shouty_snake("That world is growing in this minute.")
///     'THAT_WORLD_IS_GROWING_IN_THIS_MINUTE'
#[pyfunction]
#[pyo3(text_signature = "(s)")]
fn shouty_snake(s: &str) -> String {
    s.to_shouty_snake_case()
}

/// Convert a list of strings to SHOUTY_SNAKE_CASE.
///
/// In SHOUTY_SNAKE_CASE, word boundaries are indicated by underscores and all
/// words are in uppercase.
///
/// Example:
///     >>> from pyheck import shouty_snake_many
///     >>> shouty_snake_many(["That world is", "growing in this minute."])
///     ['THAT_WORLD_IS', 'GROWING_IN_THIS_MINUTE']
// #[pyfunction]
// #[pyo3(text_signature = "(strings)")]
// fn shouty_snake_many(strings: Vec<&str>) -> Vec<String> {
//     strings
//         .par_iter()
//         .map(|s| s.to_shouty_snake_case())
//         .collect()
// }

fn transform<F, G>(
    s: &str,
    mut with_word: F,
    mut boundary: G,
    f: &mut fmt::Formatter,
) -> fmt::Result
where
    F: FnMut(&str, &mut fmt::Formatter) -> fmt::Result,
    G: FnMut(&mut fmt::Formatter) -> fmt::Result,
{
    /// Tracks the current 'mode' of the transformation algorithm as it scans
    /// the input string.
    ///
    /// The mode is a tri-state which tracks the case of the last cased
    /// character of the current word. If there is no cased character
    /// (either lowercase or uppercase) since the previous word boundary,
    /// than the mode is `Boundary`. If the last cased character is lowercase,
    /// then the mode is `Lowercase`. Othertherwise, the mode is
    /// `Uppercase`.
    #[derive(Clone, Copy, PartialEq)]
    enum WordMode {
        /// There have been no lowercase or uppercase characters in the current
        /// word.
        Boundary,
        /// The previous cased character in the current word is lowercase.
        Lowercase,
        /// The previous cased character in the current word is uppercase.
        Uppercase,
    }

    let mut first_word = true;

    for word in s.split(|c: char| !c.is_alphanumeric()) {
        let mut char_indices = word.char_indices().peekable();
        let mut init = 0;
        let mut mode = WordMode::Boundary;

        while let Some((i, c)) = char_indices.next() {
            if let Some(&(next_i, next)) = char_indices.peek() {
                // The mode including the current character, assuming the
                // current character does not result in a word boundary.
                let next_mode = if c.is_lowercase() {
                    WordMode::Lowercase
                } else if c.is_uppercase() {
                    WordMode::Uppercase
                } else {
                    mode
                };

                // Word boundary after if current is not uppercase and next
                // is uppercase
                if next_mode == WordMode::Lowercase && next.is_uppercase() {
                    if !first_word {
                        boundary(f)?;
                    }
                    with_word(&word[init..next_i], f)?;
                    first_word = false;
                    init = next_i;
                    mode = WordMode::Boundary;

                // Otherwise if current and previous are uppercase and next
                // is lowercase, word boundary before
                } else if mode == WordMode::Uppercase && c.is_uppercase() && next.is_lowercase() {
                    if !first_word {
                        boundary(f)?;
                    } else {
                        first_word = false;
                    }
                    with_word(&word[init..i], f)?;
                    init = i;
                    mode = WordMode::Boundary;

                // Otherwise no word boundary, just update the mode
                } else {
                    mode = next_mode;
                }
            } else {
                // Collect trailing characters as a word
                if !first_word {
                    boundary(f)?;
                } else {
                    first_word = false;
                }
                with_word(&word[init..], f)?;
                break;
            }
        }
    }

    Ok(())
}

fn lowercase(s: &str, f: &mut fmt::Formatter) -> fmt::Result {
    let mut chars = s.chars().peekable();
    while let Some(c) = chars.next() {
        if c == 'Σ' && chars.peek().is_none() {
            write!(f, "ς")?;
        } else {
            write!(f, "{}", c.to_lowercase())?;
        }
    }

    Ok(())
}

fn uppercase(s: &str, f: &mut fmt::Formatter) -> fmt::Result {
    for c in s.chars() {
        write!(f, "{}", c.to_uppercase())?;
    }

    Ok(())
}

fn capitalize(s: &str, f: &mut fmt::Formatter) -> fmt::Result {
    let mut char_indices = s.char_indices();
    if let Some((_, c)) = char_indices.next() {
        write!(f, "{}", c.to_uppercase())?;
        if let Some((i, _)) = char_indices.next() {
            lowercase(&s[i..], f)?;
        }
    }

    Ok(())
}
