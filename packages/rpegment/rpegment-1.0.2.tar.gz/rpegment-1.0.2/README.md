# rpegment

`rpegment` is a package designed to segment RPE (Retinal Pigment Epithelium) confocal images using Cellpose 3 and to interactively clean the segmentation information.

## Features

- **Segmentation**: Utilizes Cellpose 3.0 [1] for accurate segmentation of RPE confocal images.
- **Interactive Cleaning**: Provides tools for interactive cleaning and refinement of segmentation results.
- **Morphology Metrics**: Visually shows a handful of metrics taken from [2], ready to download as csv.

## Installation

To install `rpegment`, you can use the following command:

```bash
pip install rpegment
```

## Usage

Here's a basic example of how to use `rpegment`:

```python
from rpegment import app

app.run(debug=True, port=8001)
```

---

## References

    @article{stringer2024cellpose3,
    title={Cellpose3: one-click image restoration for improved cellular segmentation},
    author={Stringer, Carsen and Pachitariu, Marius},
    journal={bioRxiv},
    pages={2024--02},
    year={2024},
    publisher={Cold Spring Harbor Laboratory}
    }

    @article{ortolan2022single,
    title={Single-cell--resolution map of human retinal pigment epithelium helps discover subpopulations with differential disease sensitivity},
    author={Ortolan, Davide and Sharma, Ruchi and Volkov, Andrei and Maminishkis, Arvydas and Hotaling, Nathan A and Huryn, Laryssa A and Cukras, Catherine and Di Marco, Stefano and Bisti, Silvia and Bharti, Kapil},
    journal={Proceedings of the National Academy of Sciences},
    volume={119},
    number={19},
    pages={e2117553119},
    year={2022},
    publisher={National Acad Sciences}
    }
