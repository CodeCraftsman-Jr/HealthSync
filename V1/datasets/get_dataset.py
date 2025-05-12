import os

def get_dataset(name, config):
    # Existing datasets
    if name == 'chest_xray':
        from .chest_xray import load_chest_xray
        return load_chest_xray(config)
    elif name == 'isic':
        from .isic import load_isic
        return load_isic(config)
    elif name == 'brain_mri':
        from .brain_mri import load_brain_mri
        return load_brain_mri(config)
    
    # Respiratory conditions
    elif name == 'covid19_xray':
        from .respiratory import load_covid19_xray
        return load_covid19_xray(config)
    elif name == 'tb_xray':
        from .respiratory import load_tb_xray
        return load_tb_xray(config)
    elif name == 'lung_cancer_ct':
        from .respiratory import load_lung_cancer_ct
        return load_lung_cancer_ct(config)
    
    # Neurological conditions
    elif name == 'alzheimer_mri':
        from .neurological import load_alzheimer_mri
        return load_alzheimer_mri(config)
    elif name == 'stroke_ct':
        from .neurological import load_stroke_ct
        return load_stroke_ct(config)
    elif name == 'parkinsons':
        from .neurological import load_parkinsons
        return load_parkinsons(config)
    
    # Cardiovascular conditions
    elif name == 'heart_ecg':
        from .cardiovascular import load_heart_ecg
        return load_heart_ecg(config)
    elif name == 'coronary_artery':
        from .cardiovascular import load_coronary_artery
        return load_coronary_artery(config)
    elif name == 'cardiac_mri':
        from .cardiovascular import load_cardiac_mri
        return load_cardiac_mri(config)
    
    # Gastrointestinal conditions
    elif name == 'liver_ultrasound':
        from .gastrointestinal import load_liver_ultrasound
        return load_liver_ultrasound(config)
    elif name == 'colon_cancer':
        from .gastrointestinal import load_colon_cancer
        return load_colon_cancer(config)
    elif name == 'gastric_endoscopy':
        from .gastrointestinal import load_gastric_endoscopy
        return load_gastric_endoscopy(config)
    
    # Dermatological conditions
    elif name == 'melanoma':
        from .dermatological import load_melanoma
        return load_melanoma(config)
    elif name == 'skin_disease':
        from .dermatological import load_skin_disease
        return load_skin_disease(config)
    elif name == 'psoriasis':
        from .dermatological import load_psoriasis
        return load_psoriasis(config)
    
    # Ophthalmological conditions
    elif name == 'diabetic_retinopathy':
        from .ophthalmological import load_diabetic_retinopathy
        return load_diabetic_retinopathy(config)
    elif name == 'glaucoma':
        from .ophthalmological import load_glaucoma
        return load_glaucoma(config)
    elif name == 'cataract':
        from .ophthalmological import load_cataract
        return load_cataract(config)
    
    # Orthopedic conditions
    elif name == 'knee_xray':
        from .orthopedic import load_knee_xray
        return load_knee_xray(config)
    elif name == 'bone_fracture':
        from .orthopedic import load_bone_fracture
        return load_bone_fracture(config)
    elif name == 'spine_mri':
        from .orthopedic import load_spine_mri
        return load_spine_mri(config)
    
    # Dental conditions
    elif name == 'dental_xray':
        from .dental import load_dental_xray
        return load_dental_xray(config)
    elif name == 'dental_caries':
        from .dental import load_dental_caries
        return load_dental_caries(config)
    elif name == 'oral_cancer':
        from .dental import load_oral_cancer
        return load_oral_cancer(config)
    
    # Endocrine conditions
    elif name == 'thyroid_ultrasound':
        from .endocrine import load_thyroid_ultrasound
        return load_thyroid_ultrasound(config)
    elif name == 'diabetes_retinal':
        from .endocrine import load_diabetes_retinal
        return load_diabetes_retinal(config)
    
    # Gynecological conditions
    elif name == 'cervical_cancer':
        from .gynecological import load_cervical_cancer
        return load_cervical_cancer(config)
    elif name == 'breast_cancer':
        from .gynecological import load_breast_cancer
        return load_breast_cancer(config)
    elif name == 'breast_mammography':
        from .gynecological import load_breast_mammography
        return load_breast_mammography(config)
    
    # Urological conditions
    elif name == 'kidney_stone':
        from .urological import load_kidney_stone
        return load_kidney_stone(config)
    elif name == 'prostate_cancer':
        from .urological import load_prostate_cancer
        return load_prostate_cancer(config)
    
    # Pediatric conditions
    elif name == 'pediatric_pneumonia':
        from .pediatric import load_pediatric_pneumonia
        return load_pediatric_pneumonia(config)
    elif name == 'bone_age':
        from .pediatric import load_bone_age
        return load_bone_age(config)
    
    # Infectious diseases
    elif name == 'malaria':
        from .infectious import load_malaria
        return load_malaria(config)
    elif name == 'covid19_ct':
        from .infectious import load_covid19_ct
        return load_covid19_ct(config)
    
    # Hematological conditions
    elif name == 'blood_cells':
        from .hematological import load_blood_cells
        return load_blood_cells(config)
    elif name == 'leukemia':
        from .hematological import load_leukemia
        return load_leukemia(config)
    
    # Miscellaneous
    elif name == 'nerve_ultrasound':
        from .miscellaneous import load_nerve_ultrasound
        return load_nerve_ultrasound(config)
    elif name == 'medical_mnist':
        from .miscellaneous import load_medical_mnist
        return load_medical_mnist(config)
    elif name == 'liver_segmentation':
        from .miscellaneous import load_liver_segmentation
        return load_liver_segmentation(config)
    elif name == 'brain_segmentation':
        from .miscellaneous import load_brain_segmentation
        return load_brain_segmentation(config)
    
    else:
        raise ValueError(f"Unknown dataset: {name}")

