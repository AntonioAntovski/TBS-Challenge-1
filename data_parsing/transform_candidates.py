def transform_candidates(candidates):
    candidates_ = [
        {
            "name": candidate.name,
            "birth_date": candidate.birth_date,
            "locations": [
                {
                    "city": location.city,
                    "country": location.country
                }
                for location in candidate.locations
            ],
            "skills": [
                {
                    "name": skill.name,
                    "obtained": skill.obtained
                }
                for skill in candidate.skills
            ],
            "jobs": [
                {
                    "title": job.title,
                    "start": job.start,
                    "end": job.end,
                    "description": job.description
                }
                for job in candidate.jobs
            ]
        }
        for candidate in candidates
    ]

    return candidates_
