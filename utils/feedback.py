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

    report = {}
    for angle_name, score in angle_scores.items():
        try:
            issue = ""
            condition = None
            if score > 40:
                condition = "big more"
            elif score > 20:
                condition = "more"
            elif score < -40:
                condition = "big less"
            elif score < -20:
                condition = "less"
            if condition:
                issue = get_angle_feedback(angle_name, stage, condition)
                report[angle_name] = {"condition": condition, "feedback": issue}
        except (KeyError, TypeError):
            continue

    return report

def get_angle_feedback(angle_name, stage, condition):
    """
    Returns issue description and correction for a specific angle deviation.

    Args:
        angle_name: Str, name of the angle (e.g., "right_elbow_angle").
        stage: Str, shooting stage ("loading", "gather", "release", "follow").
        condition: Str, "big more", "more", "big less", or "less".

    Returns:
        Tuple of (issue_description, correction_suggestion).
    """
    feedback = {
        "right_elbow_angle": {
            "loading": {
                "big more": ("Severely extended elbow leads to ball loaded too low, slowing release.",
                             "Significantly bend elbow to keep ball at chest level for fluid motion."),
                "more": ("Extended elbow causes ball to load too low, slowing release.",
                         "Bend elbow to position ball at chest for smoother shot setup."),
                "big less": ("Severely excessive elbow bend pulls ball too low, disrupting fluidity.",
                             "Greatly reduce elbow bend to maintain compact shot motion."),
                "less": ("Excessive elbow bend pulls ball below chest, slowing release.",
                         "Reduce elbow bend to keep ball at chest level.")
            },
            "gather": {
                "big more": ("Severely flared elbow disrupts alignment, causing major accuracy loss.",
                             "Keep elbow tightly tucked to align with basket."),
                "more": ("Flared elbow reduces shot accuracy due to misalignment.",
                         "Tuck elbow in for proper alignment with the basket."),
                "big less": ("Severely bent elbow delays shot preparation, rushing release.",
                             "Extend elbow significantly for smooth transition to release."),
                "less": ("Overly bent elbow slows shot setup, affecting rhythm.",
                         "Extend elbow slightly for better shot preparation.")
            },
            "release": {
                "big more": ("Severely early extension leads to low release point, flattening trajectory.",
                             "Maintain significant elbow bend for higher release and better arc."),
                "more": ("Early extension causes low release point, reducing arc.",
                         "Keep slight elbow bend for higher release point."),
                "big less": ("Severely incomplete extension results in low release, drastically reducing power.",
                             "Fully extend elbow at release for maximum power and height."),
                "less": ("Incomplete extension lowers release point, reducing power.",
                         "Extend elbow more at release for improved power.")
            },
            "follow": {
                "big more": ("Severely stiff elbow reduces follow-through fluidity, affecting consistency.",
                             "Fully extend but relax elbow for smooth, consistent follow-through."),
                "more": ("Stiff elbow shortens follow-through, reducing consistency.",
                         "Extend and relax elbow for smooth follow-through."),
                "big less": ("Severely abbreviated follow-through disrupts shot consistency critically.",
                             "Fully extend elbow toward rim for consistent follow-through."),
                "less": ("Abbreviated follow-through affects shot consistency.",
                         "Extend elbow fully toward rim for better follow-through.")
            }
        },
        "right_wrist_angle": {
            "loading": {
                "big more": ("Severely rigid wrist misaligns ball, disrupting setup.",
                             "Maintain neutral wrist position to align ball properly."),
                "more": ("Rigid wrist limits snap potential, misaligning ball.",
                         "Keep wrist neutral for proper ball positioning."),
                "big less": ("Severely flexed wrist pulls ball too low, slowing shot.",
                             "Reduce wrist flexion significantly for proper setup."),
                "less": ("Flexed wrist misaligns ball, affecting setup.",
                         "Reduce wrist flexion for proper positioning.")
            },
            "gather": {
                "big more": ("Severely extended wrist causes improper grip, leading to major control loss.",
                             "Keep wrist neutral for firm, relaxed ball grip."),
                "more": ("Extended wrist affects grip, reducing ball control.",
                         "Maintain neutral wrist for proper grip."),
                "big less": ("Severely flexed wrist disrupts grip, causing fumbling.",
                             "Reduce wrist flexion significantly for stable grip."),
                "less": ("Flexed wrist affects grip consistency.",
                         "Keep wrist neutral for better ball control.")
            },
            "release": {
                "big more": ("Severely insufficient wrist snap eliminates backspin, flattening shot.",
                             "Snap wrist significantly for strong backspin and arc."),
                "more": ("Insufficient wrist snap reduces backspin, affecting arc.",
                         "Snap wrist more for added backspin."),
                "big less": ("Severely excessive snap causes erratic release, reducing accuracy.",
                             "Moderate wrist snap significantly for controlled release."),
                "less": ("Excessive wrist snap may cause erratic release.",
                         "Moderate wrist snap for better control.")
            },
            "follow": {
                "big more": ("Severely inadequate follow-through eliminates spin, flattening shot.",
                             "Flex wrist downward significantly after release for backspin."),
                "more": ("Inadequate follow-through reduces spin, affecting arc.",
                         "Flex wrist downward after release for better arc."),
                "big less": ("Severely over-snapped wrist disrupts shot consistency.",
                             "Moderate wrist snap for consistent follow-through."),
                "less": ("Over-snapped wrist affects shot consistency.",
                         "Ensure smooth downward wrist snap.")
            }
        },
        "right_shoulder_angle": {
            "loading": {
                "big more": ("Severely raised shoulder pushes ball too low, slowing release.",
                             "Lower shoulder significantly to align ball at chest."),
                "more": ("Raised shoulder causes ball to load too low, affecting fluidity.",
                         "Lower shoulder to keep ball at chest level."),
                "big less": ("Severely low shoulder misaligns ball, disrupting setup.",
                             "Elevate shoulder significantly for proper ball positioning."),
                "less": ("Low shoulder limits ball positioning.",
                         "Elevate shoulder slightly for better setup.")
            },
            "gather": {
                "big more": ("Severely raised shoulder disrupts body alignment, causing major accuracy loss.",
                             "Lower shoulder significantly for consistent setup."),
                "more": ("Raised shoulder disrupts alignment, reducing accuracy.",
                         "Keep shoulder lower for consistent setup."),
                "big less": ("Severely low shoulder delays ball elevation, rushing shot.",
                             "Raise shoulder significantly for proper positioning."),
                "less": ("Low shoulder limits ball elevation.",
                         "Raise shoulder slightly for proper positioning.")
            },
            "release": {
                "big more": ("Severely raised shoulder causes low release point, straining shot.",
                             "Relax shoulder significantly for higher release and consistency."),
                "more": ("Raised shoulder lowers release point, straining shot.",
                         "Relax shoulder for higher release point."),
                "big less": ("Severely low shoulder drastically limits shot height and power.",
                             "Elevate shoulder significantly for added power and height."),
                "less": ("Low shoulder limits shot height.",
                         "Elevate shoulder for added power.")
            },
            "follow": {
                "big more": ("Severely tense shoulder reduces follow-through fluidity, affecting consistency.",
                             "Relax shoulder significantly for smooth follow-through."),
                "more": ("Tense shoulder reduces follow-through smoothness.",
                         "Keep shoulder relaxed for smooth follow-through."),
                "big less": ("Severely low shoulder weakens follow-through, reducing arc.",
                             "Elevate shoulder significantly for complete follow-through."),
                "less": ("Low shoulder weakens follow-through arc.",
                         "Elevate shoulder for complete follow-through.")
            }
        },
        "right_hip_angle": {
            "loading": {
                "big more": ("Severely straight hips create unstable base, drastically reducing power.",
                             "Bend hips significantly for a balanced, athletic stance."),
                "more": ("Straight hips cause unstable base, reducing power.",
                         "Bend hips more for increased power and balance."),
                "big less": ("Severely excessive hip bend causes major instability, disrupting shot.",
                             "Reduce hip bend significantly for better mobility and stability."),
                "less": ("Excessive hip bend unbalances stance.",
                         "Reduce hip bend slightly for better balance.")
            },
            "gather": {
                "big more": ("Severely premature hip extension disrupts timing, causing imbalance.",
                             "Maintain significant hip bend for balanced transition."),
                "more": ("Premature hip extension disrupts shot timing.",
                         "Maintain slight hip bend for balance."),
                "big less": ("Severely delayed hip extension slows shot rhythm critically.",
                             "Extend hips significantly for smoother transition."),
                "less": ("Delayed hip extension affects shot rhythm.",
                         "Extend hips slightly for smoother transition.")
            },
            "release": {
                "big more": ("Severely overextended hips cause backward lean, losing balance.",
                             "Extend hips fully while maintaining significant balance."),
                "more": ("Overextended hips may cause backward lean.",
                         "Fully extend hips while maintaining balance."),
                "big less": ("Severely incomplete hip extension drastically reduces shot power.",
                             "Fully extend hips for maximum jump power."),
                "less": ("Incomplete hip extension reduces power.",
                         "Fully extend hips for maximum jump power.")
            },
            "follow": {
                "big more": ("Severely overextended hips cause major balance loss on landing.",
                             "Extend hips fully but maintain significant balance for stable landing."),
                "more": ("Overextended hips affect landing balance.",
                         "Extend hips fully but stay balanced."),
                "big less": ("Severely incomplete hip extension causes unstable landing.",
                             "Fully extend hips for stable, balanced landing."),
                "less": ("Incomplete hip extension reduces landing stability.",
                         "Fully extend hips for stable landing.")
            }
        },
        "right_knee_angle": {
            "loading": {
                "big more": ("Severely straight knees create unstable base, drastically reducing power.",
                             "Bend knees significantly for explosive jump and stability."),
                "more": ("Insufficient knee bend reduces power and stability.",
                         "Bend knees more for explosive jump."),
                "big less": ("Severely excessive knee bend causes major instability, slowing shot.",
                             "Reduce knee bend significantly for better mobility and balance."),
                "less": ("Excessive knee bend unbalances stance.",
                         "Reduce knee bend slightly for better balance.")
            },
            "gather": {
                "big more": ("Severely premature knee extension disrupts shot rhythm critically.",
                             "Maintain significant knee bend for proper timing."),
                "more": ("Premature knee straightening disrupts shot rhythm.",
                         "Maintain slight knee bend for proper timing."),
                "big less": ("Severely delayed knee extension slows transition, rushing shot.",
                             "Extend knees significantly for smoother transition."),
                "less": ("Delayed knee extension affects rhythm.",
                         "Extend knees slightly for smoother transition.")
            },
            "release": {
                "big more": ("Severely overextended knees cause imbalance, reducing shot power.",
                             "Fully extend knees while maintaining significant balance."),
                "more": ("Overextended knees may cause imbalance.",
                         "Fully extend knees while maintaining balance."),
                "big less": ("Severely incomplete knee extension drastically limits shot elevation.",
                             "Fully extend knees for maximum shot power."),
                "less": ("Incomplete knee drive reduces elevation.",
                         "Fully extend knees for maximum shot power.")
            },
            "follow": {
                "big more": ("Severely overextended knees cause major balance loss on landing.",
                             "Extend knees fully with significant balance for stable landing."),
                "more": ("Overextended knees affect landing balance.",
                         "Extend knees fully but stay balanced."),
                "big less": ("Severely incomplete knee extension causes unstable landing.",
                             "Fully extend knees for stable, balanced landing."),
                "less": ("Incomplete knee drive reduces landing stability.",
                         "Fully extend knees for balanced landing.")
            }
        },
        "left_elbow_angle": {
            "loading": {
                "big more": ("Severely extended guide elbow pushes ball off-center, disrupting setup.",
                             "Bend guide elbow significantly to stabilize ball."),
                "more": ("Extended guide elbow pushes ball off-center.",
                         "Keep guide elbow slightly bent to stabilize ball."),
                "big less": ("Severely bent guide elbow interferes with shooting hand, slowing shot.",
                             "Extend guide elbow significantly for better control."),
                "less": ("Overly bent guide elbow interferes with shooting hand.",
                         "Extend guide elbow slightly for better control.")
            },
            "gather": {
                "big more": ("Severely flared guide elbow disrupts alignment, causing major accuracy loss.",
                             "Keep guide elbow tightly tucked for proper setup."),
                "more": ("Flared guide elbow affects shot alignment.",
                         "Keep guide elbow slightly bent for proper setup."),
                "big less": ("Severely bent guide elbow delays shot setup, rushing release.",
                             "Extend guide elbow significantly for alignment."),
                "less": ("Overly bent guide elbow slows shot preparation.",
                         "Extend guide elbow slightly for alignment.")
            },
            "release": {
                "big more": ("Severely extended guide elbow causes thumb flick, disrupting trajectory.",
                             "Relax guide elbow significantly to avoid interference."),
                "more": ("Extended guide elbow pushes ball, affecting trajectory.",
                         "Relax guide elbow to avoid interference."),
                "big less": ("Severely bent guide elbow interferes with release, causing side spin.",
                             "Extend guide elbow slightly for clean release."),
                "less": ("Bent guide elbow interferes with shot release.",
                         "Extend guide elbow slightly for stability.")
            },
            "follow": {
                "big more": ("Severely extended guide elbow lingers, disrupting shot consistency.",
                             "Relax guide elbow significantly to complete follow-through."),
                "more": ("Lingering guide elbow affects shot alignment.",
                         "Relax guide elbow to complete follow-through."),
                "big less": ("Severely bent guide elbow disrupts follow-through balance.",
                             "Maintain slight bend in guide elbow for smooth follow-through."),
                "less": ("Overly bent guide elbow affects follow-through.",
                         "Maintain slight bend in guide elbow.")
            }
        },
        "left_wrist_angle": {
            "loading": {
                "big more": ("Severely extended guide wrist pushes ball off-line, disrupting setup.",
                             "Keep guide wrist neutral to avoid interference."),
                "more": ("Extended guide wrist pushes ball off-line.",
                         "Keep guide wrist neutral to avoid interference."),
                "big less": ("Severely flexed guide wrist grips too tightly, slowing shot.",
                             "Reduce guide wrist flexion significantly for proper positioning."),
                "less": ("Flexed guide wrist affects ball positioning.",
                         "Reduce guide wrist flexion for proper positioning.")
            },
            "gather": {
                "big more": ("Severely extended guide wrist disrupts grip, causing major control loss.",
                             "Maintain neutral guide wrist for firm, relaxed grip."),
                "more": ("Extended guide wrist affects grip, reducing control.",
                         "Maintain neutral guide wrist for setup."),
                "big less": ("Severely flexed guide wrist causes fumbling, disrupting shot.",
                             "Keep guide wrist neutral for stable grip."),
                "less": ("Flexed guide wrist affects grip consistency.",
                         "Keep guide wrist neutral for alignment.")
            },
            "release": {
                "big more": ("Severely extended guide wrist causes thumb flick, disrupting trajectory.",
                             "Keep guide wrist neutral to avoid interference."),
                "more": ("Extended guide wrist pushes ball off-line.",
                         "Keep guide wrist neutral to avoid interference."),
                "big less": ("Severely flexed guide wrist grips too tightly, causing side spin.",
                             "Maintain neutral guide wrist for clean release."),
                "less": ("Flexed guide wrist affects release accuracy.",
                         "Maintain neutral guide wrist for clean release.")
            },
            "follow": {
                "big more": ("Severely extended guide wrist lingers, disrupting shot consistency.",
                             "Relax guide wrist significantly to complete follow-through."),
                "more": ("Lingering guide wrist affects shot stability.",
                         "Relax guide wrist to complete follow-through."),
                "big less": ("Severely flexed guide wrist disrupts follow-through balance.",
                             "Maintain neutral guide wrist for consistent follow-through."),
                "less": ("Flexed guide wrist affects follow-through stability.",
                         "Maintain neutral guide wrist position.")
            }
        },
        "left_shoulder_angle": {
            "loading": {
                "big more": ("Severely raised guide shoulder pushes ball off-center, slowing setup.",
                             "Lower guide shoulder significantly to stabilize ball."),
                "more": ("Raised guide shoulder misaligns ball, affecting setup.",
                         "Lower guide shoulder to keep ball at chest level."),
                "big less": ("Severely low guide shoulder disrupts ball positioning, slowing shot.",
                             "Elevate guide shoulder significantly for proper setup."),
                "less": ("Low guide shoulder limits ball positioning.",
                         "Elevate guide shoulder slightly for better setup.")
            },
            "gather": {
                "big more": ("Severely raised guide shoulder disrupts alignment, causing major accuracy loss.",
                             "Lower guide shoulder significantly for consistent setup."),
                "more": ("Raised guide shoulder affects shot alignment.",
                         "Keep guide shoulder lower for consistent setup."),
                "big less": ("Severely low guide shoulder delays ball elevation, rushing shot.",
                             "Raise guide shoulder significantly for proper positioning."),
                "less": ("Low guide shoulder limits ball elevation.",
                         "Raise guide shoulder slightly for proper positioning.")
            },
            "release": {
                "big more": ("Severely raised guide shoulder interferes with release, reducing arc.",
                             "Relax guide shoulder significantly for clean release."),
                "more": ("Raised guide shoulder lowers release point.",
                         "Relax guide shoulder for higher release."),
                "big less": ("Severely low guide shoulder disrupts release, reducing power.",
                             "Elevate guide shoulder significantly for stable release."),
                "less": ("Low guide shoulder affects release height.",
                         "Elevate guide shoulder for added power.")
            },
            "follow": {
                "big more": ("Severely tense guide shoulder reduces follow-through fluidity.",
                             "Relax guide shoulder significantly for smooth follow-through."),
                "more": ("Tense guide shoulder affects follow-through smoothness.",
                         "Keep guide shoulder relaxed for smooth follow-through."),
                "big less": ("Severely low guide shoulder weakens follow-through, reducing consistency.",
                             "Elevate guide shoulder significantly for complete follow-through."),
                "less": ("Low guide shoulder affects follow-through arc.",
                         "Elevate guide shoulder for complete follow-through.")
            }
        },
        "left_hip_angle": {
            "loading": {
                "big more": ("Severely straight guide hip creates unstable base, drastically reducing balance.",
                             "Bend guide hip significantly for a stable, athletic stance."),
                "more": ("Straight guide hip reduces stance stability.",
                         "Bend guide hip more for balanced stance."),
                "big less": ("Severely excessive guide hip bend causes major imbalance.",
                             "Reduce guide hip bend significantly for better balance."),
                "less": ("Excessive guide hip bend unbalances stance.",
                         "Reduce guide hip bend slightly for better balance.")
            },
            "gather": {
                "big more": ("Severely premature guide hip extension disrupts balance, affecting rhythm.",
                             "Maintain significant guide hip bend for symmetry."),
                "more": ("Premature guide hip extension affects balance.",
                         "Maintain slight guide hip bend for symmetry."),
                "big less": ("Severely delayed guide hip extension slows transition, disrupting shot.",
                             "Extend guide hip significantly for balanced transition."),
                "less": ("Delayed guide hip extension affects rhythm.",
                         "Extend guide hip slightly for smoother transition.")
            },
            "release": {
                "big more": ("Severely overextended guide hip causes major imbalance.",
                             "Extend guide hip fully with significant symmetry for stability."),
                "more": ("Overextended guide hip causes imbalance.",
                         "Fully extend guide hip symmetrically for stability."),
                "big less": ("Severely incomplete guide hip extension reduces stability drastically.",
                             "Fully extend guide hip for maximum power and stability."),
                "less": ("Incomplete guide hip extension reduces stability.",
                         "Fully extend guide hip for maximum power.")
            },
            "follow": {
                "big more": ("Severely overextended guide hip causes major balance loss on landing.",
                             "Extend guide hip fully with significant symmetry for stable landing."),
                "more": ("Overextended guide hip affects landing balance.",
                         "Extend guide hip fully with symmetry for stable landing."),
                "big less": ("Severely incomplete guide hip extension causes unstable landing.",
                             "Fully extend guide hip for balanced landing."),
                "less": ("Incomplete guide hip extension reduces landing stability.",
                         "Fully extend guide hip for balanced landing.")
            }
        },
        "left_knee_angle": {
            "loading": {
                "big more": ("Severely straight guide knee creates unstable base, drastically reducing balance.",
                             "Bend guide knee significantly for a stable, athletic stance."),
                "more": ("Straight guide knee reduces stance stability.",
                         "Bend guide knee more for balanced stance."),
                "big less": ("Severely excessive guide knee bend causes major imbalance.",
                             "Reduce guide knee bend significantly for better balance."),
                "less": ("Excessive guide knee bend unbalances stance.",
                         "Reduce guide knee bend slightly for better balance.")
            },
            "gather": {
                "big more": ("Severely premature guide knee extension disrupts rhythm, causing imbalance.",
                             "Maintain significant guide knee bend for proper timing."),
                "more": ("Premature guide knee extension affects shot rhythm.",
                         "Maintain slight guide knee bend for proper timing."),
                "big less": ("Severely delayed guide knee extension slows transition, rushing shot.",
                             "Extend guide knee significantly for smoother transition."),
                "less": ("Delayed guide knee extension affects rhythm.",
                         "Extend guide knee slightly for smoother transition.")
            },
            "release": {
                "big more": ("Severely overextended guide knee causes major imbalance.",
                             "Fully extend guide knee with significant symmetry for stability."),
                "more": ("Overextended guide knee causes imbalance.",
                         "Fully extend guide knee symmetrically for stability."),
                "big less": ("Severely incomplete guide knee extension reduces stability drastically.",
                             "Fully extend guide knee for maximum power and stability."),
                "less": ("Incomplete guide knee drive affects stability.",
                         "Fully extend guide knee for maximum power.")
            },
            "follow": {
                "big more": ("Severely overextended guide knee causes major balance loss on landing.",
                             "Extend guide knee fully with significant symmetry for stable landing."),
                "more": ("Overextended guide knee affects landing balance.",
                         "Extend guide knee fully with symmetry for stable landing."),
                "big less": ("Severely incomplete guide knee extension causes unstable landing.",
                             "Fully extend guide knee for balanced landing."),
                "less": ("Incomplete guide knee drive reduces landing stability.",
                         "Fully extend guide knee for balanced landing.")
            }
        }
    }

    return feedback.get(angle_name, {}).get(stage, {}).get(condition, ("", ""))

if __name__ == "__main__":
    example_differences = {
        "right_elbow_angle": 50,    # Triggers "big more"
        "right_wrist_angle": 24.38, # Triggers "more"
        "right_shoulder_angle": -6.6, # No trigger
        "right_hip_angle": -45,     # Triggers "big less"
        "right_knee_angle": -21.27, # Triggers "less"
        "left_elbow_angle": 5.38,   # No trigger
        "left_wrist_angle": -8.69,  # No trigger
        "left_hip_angle": -51.31,   # Triggers "big less"
        "left_knee_angle": -56.02   # Triggers "big less"
    }
    analysis = analyze_shot_form(example_differences, stage="release")
    print("# Basketball Shot Form Analysis\n")
    for angle, data in analysis.items():
        condition, (issue, correction) = data["condition"], data["feedback"]
        print(f"**{angle.replace('_', ' ').title()}** ({condition})")
        print(f"- Issue: {issue}")
        print(f"- Correction: {correction}\n")