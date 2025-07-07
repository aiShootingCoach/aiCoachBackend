weights = {
    "loading": {
        "Right": {
            "Wrist": 4,
            "Elbow": 7,
            "Shoulder": 9,
            "Hip": 8,
            "Knee": 7
        },
        "Left": {
            "Wrist": 3,
            "Elbow": 6,
            "Shoulder": 7,
            "Hip": 8,
            "Knee": 7
        }
    },
    "gather": {
        "Right": {
            "Wrist": 8,
            "Elbow": 10,
            "Shoulder": 8,
            "Hip": 9,
            "Knee": 9
        },
        "Left": {
            "Wrist": 4,
            "Elbow": 8,
            "Shoulder": 7,
            "Hip": 9,
            "Knee": 9
        }
    },
    "release": {
        "Right": {
            "Wrist": 10,
            "Elbow": 9,
            "Shoulder": 10,
            "Hip": 5,
            "Knee": 6
        },
        "Left": {
            "Wrist": 5,
            "Elbow": 6,
            "Shoulder": 7,
            "Hip": 5,
            "Knee": 6
        }
    },
    "follow": {
        "Right": {
            "Wrist": 9,
            "Elbow": 9 ,
            "Shoulder": 9,
            "Hip": 6,
            "Knee": 5
        },
        "Left": {
            "Wrist": 9,
            "Elbow": 9,
            "Shoulder": 9,
            "Hip": 6,
            "Knee": 5
        }
    }
}
def analyze_shot_form(angle_differences, stage=None):
    if angle_differences is None:
        return {}

    if stage is None or stage not in weights:
        stage = "release"  # Default to release stage

    angle_scores = {}
    required_angles = [
        "right_elbow_angle", "right_wrist_angle", "right_shoulder_angle",
        "right_hip_angle", "right_knee_angle", "left_elbow_angle",
        "left_wrist_angle", "left_shoulder_angle", "left_hip_angle",
        "left_knee_angle"
    ]

    for angle in required_angles:
        if angle not in angle_differences or angle_differences[angle] is None:
            continue
        if angle.startswith("right_"):
            side = "Right"
            joint = angle.replace("right_", "").replace("_angle", "").capitalize()
        else:
            side = "Left"
            joint = angle.replace("left_", "").replace("_angle", "").capitalize()
        angle_scores[angle] = angle_differences[angle] * weights[stage][side][joint]
    title = "# Basketball Shot Form Analysis\n\n"
    report = {}
    for angle_name, score in angle_scores.items():
        try:
            issue = ""
            if score > 40:
                condition = "more"
                issue = get_angle_feedback(angle_name, stage, condition)
            elif score < -40:
                condition = "less"
                issue = get_angle_feedback(angle_name, stage, condition)
            if issue != "":
                report[angle_name] = issue
        except (KeyError, TypeError):
            continue

    return report


def get_angle_feedback(angle_name, stage, condition):
    """
    Returns issue description and correction for a specific angle deviation.

    Args:
        angle_name: Str, name of the angle (e.g., "right_elbow_angle").
        stage: Str, shooting stage ("loading", "gather", "release", "follow").
        condition: Str, "more" (too extended) or "less" (too flexed).

    Returns:
        Tuple of (issue_description, correction_suggestion).
    """
    feedback = {
        "right_elbow_angle": {
            "loading": {
                "more": ("Reduces power storage due to insufficient bend.",
                         "Bend the elbow more to store energy for the shot."),
                "less": ("Excessive bend misaligns the ball.",
                         "Reduce elbow bend slightly for proper ball positioning.")
            },
            "gather": {
                "more": ("Premature extension disrupts shot timing.",
                         "Keep elbow tucked for smooth transition to release."),
                "less": ("Delays shot preparation, causing rushed release.",
                         "Extend elbow slightly for better alignment.")
            },
            "release": {
                "more": ("Early extension leads to flat trajectory.",
                         "Release with a slight elbow bend for better arc."),
                "less": ("Incomplete extension reduces power.", "Extend elbow more at release for improved power.")
            },
            "follow": {
                "more": ("Excessive stiffness reduces fluidity.",
                         "Fully extend elbow but keep relaxed for smooth follow."),
                "less": ("Incomplete follow affects consistency.",
                         "Fully extend elbow for consistent follow.")
            }
        },
        "right_wrist_angle": {
            "loading": {
                "more": ("Rigid wrist limits snap potential.", "Maintain neutral wrist position."),
                "less": ("Misaligns ball, affecting setup.", "Reduce wrist flexion for proper positioning.")
            },
            "gather": {
                "more": ("Limits wrist snap potential.", "Keep wrist neutral for smooth transition."),
                "less": ("Misaligns ball, disrupting release.", "Maintain neutral wrist position.")
            },
            "release": {
                "more": ("Insufficient snap reduces spin.", "Snap wrist more for added backspin."),
                "less": ("Excessive snap may cause erratic release.", "Moderate wrist snap for better control.")
            },
            "follow": {
                "more": ("Lack of downward snap reduces arc.", "Flex wrist downward after release for better arc."),
                "less": ("Over-snap may affect consistency.", "Ensure smooth downward wrist snap.")
            }
        },
        "right_shoulder_angle": {
            "loading": {
                "more": ("Pushes ball too far forward.", "Keep shoulder lower for proper alignment."),
                "less": ("Limits ball positioning.", "Elevate shoulder slightly for better setup.")
            },
            "gather": {
                "more": ("Disrupts body alignment.", "Keep shoulder lower for consistent setup."),
                "less": ("Limits ball elevation.", "Raise shoulder slightly for proper positioning.")
            },
            "release": {
                "more": ("Strains shoulder, reducing consistency.", "Relax shoulder during release."),
                "less": ("Limits shot height.", "Elevate shoulder for added power.")
            },
            "follow": {
                "more": ("Causes tension, reducing smoothness.", "Keep shoulder relaxed for smooth follow."),
                "less": ("Weak follow limits arc.", "Elevate shoulder for complete follow.")
            }
        },
        "right_hip_angle": {
            "loading": {
                "more": ("Shallow squat reduces jump power.", "Bend hips more for increased power."),
                "less": ("Excessive bend limits mobility.", "Reduce hip bend slightly for better mobility.")
            },
            "gather": {
                "more": ("Premature extension disrupts timing.", "Maintain slight hip bend for balance."),
                "less": ("Delays rise, affecting rhythm.", "Extend hips slightly for smoother transition.")
            },
            "release": {
                "more": ("Overextension may cause backward lean.", "Fully extend hips while maintaining balance."),
                "less": ("Incomplete extension reduces power.", "Fully extend hips for maximum jump power.")
            },
            "follow": {
                "more": ("Backward lean disrupts balance.", "Extend hips fully but stay balanced."),
                "less": ("Incomplete extension affects stability.", "Fully extend hips for stable landing.")
            }
        },
        "right_knee_angle": {
            "loading": {
                "more": ("Shallow bend reduces power.", "Bend knees more for explosive jump."),
                "less": ("Excessive bend slows movement.", "Reduce knee bend slightly for better mobility.")
            },
            "gather": {
                "more": ("Premature straightening disrupts rhythm.", "Maintain slight knee bend for proper timing."),
                "less": ("Slows transition to release.", "Extend knees slightly for smoother transition.")
            },
            "release": {
                "more": ("Overextension may cause imbalance.", "Fully extend knees while maintaining balance."),
                "less": ("Incomplete drive limits elevation.", "Fully extend knees for maximum shot power.")
            },
            "follow": {
                "more": ("Overextension affects landing.", "Extend knees fully but stay balanced."),
                "less": ("Incomplete drive affects stability.", "Fully extend knees for stable landing.")
            }
        },
        "left_elbow_angle": {
            "loading": {
                "more": ("Pushes ball off-center.", "Keep guide elbow slightly bent to stabilize ball."),
                "less": ("Interferes with shooting hand.", "Extend guide elbow slightly for better control.")
            },
            "gather": {
                "more": ("Pushes ball, affecting alignment.", "Keep guide elbow slightly bent for proper setup."),
                "less": ("Interferes with shot setup.", "Extend guide elbow slightly for alignment.")
            },
            "release": {
                "more": ("Pushes ball, disrupting trajectory.", "Relax guide elbow to avoid interference."),
                "less": ("Interferes with release.", "Extend guide elbow slightly for stability.")
            },
            "follow": {
                "more": ("Lingering guide hand affects alignment.", "Relax guide elbow to complete follow."),
                "less": ("Premature withdrawal disrupts balance.", "Maintain slight bend in guide elbow.")
            }
        },
        "left_wrist_angle": {
            "loading": {
                "more": ("Pushes ball off-line.", "Keep guide wrist neutral to avoid interference."),
                "less": ("Grips too tightly, affecting shot.", "Reduce guide wrist flexion for proper positioning.")
            },
            "gather": {
                "more": ("Pushes ball, reducing accuracy.", "Maintain neutral guide wrist for setup."),
                "less": ("Interferes with setup.", "Keep guide wrist neutral for alignment.")
            },
            "release": {
                "more": ("Pushes ball off-line.", "Keep guide wrist neutral to avoid interference."),
                "less": ("Grips too tightly, affecting release.", "Maintain neutral guide wrist for clean release.")
            },
            "follow": {
                "more": ("Lingering interference with shot.", "Relax guide wrist to complete follow."),
                "less": ("Premature withdrawal affects stability.", "Maintain neutral guide wrist position.")
            }
        },
        "left_hip_angle": {
            "loading": {
                "more": ("Shallow bend reduces balance.", "Bend hips more for stable stance."),
                "less": ("Excessive bend unbalances stance.", "Reduce hip bend slightly for better balance.")
            },
            "gather": {
                "more": ("Asymmetry disrupts balance.", "Maintain slight hip bend for symmetry."),
                "less": ("Uneven posture affects rhythm.", "Extend hips slightly for balanced transition.")
            },
            "release": {
                "more": ("Asymmetry causes imbalance.", "Fully extend hips symmetrically for stability."),
                "less": ("Uneven extension reduces stability.", "Fully extend hips for maximum power.")
            },
            "follow": {
                "more": ("Asymmetry affects landing.", "Extend hips fully with symmetry for stable landing."),
                "less": ("Uneven extension reduces stability.", "Fully extend hips for balanced landing.")
            }
        },
        "left_knee_angle": {
            "loading": {
                "more": ("Shallow bend reduces stability.", "Bend knees more for balanced stance."),
                "less": ("Excessive bend unbalances stance.", "Reduce knee bend slightly for better balance.")
            },
            "gather": {
                "more": ("Premature extension disrupts rhythm.", "Maintain slight knee bend for proper timing."),
                "less": ("Uneven posture affects balance.", "Extend knees slightly for smoother transition.")
            },
            "release": {
                "more": ("Asymmetry causes imbalance.", "Fully extend knees symmetrically for stability."),
                "less": ("Uneven drive affects stability.", "Fully extend knees for maximum power.")
            },
            "follow": {
                "more": ("Asymmetry affects landing.", "Extend knees fully with symmetry for stable landing."),
                "less": ("Uneven drive reduces stability.", "Fully extend knees for balanced landing.")
            }
        }
    }

    return feedback[angle_name][stage][condition]


# Example usage:
if __name__ == "__main__":
    example_differences = {
        "right_elbow_angle": 37.66,  # Example: player angle too extended
        "right_wrist_angle": 24.38,  # Too extended
        "right_shoulder_angle": -6.6,  # Too flexed
        "right_hip_angle": -5.52,  # Too flexed
        "right_knee_angle": -21.27,  # Too flexed
        "left_elbow_angle": 5.38,  # Too extended
        "left_wrist_angle": -8.69,  # Too flexed
        "left_hip_angle": -51.31,  # Too flexed
        "left_knee_angle": -56.02  # Too flexed
    }
    analysis = analyze_shot_form(example_differences, stage="release")
    print(analysis)