from imgaug import augmenters as iaa
import configparser
import tempfile

# 從config中讀取相對應的參數並選擇一個augmentation function
# noise function
def get_noise_fn(config):
    # OneOf function提供選擇一個augmentation function的功用
    aug = iaa.OneOf([])

    # AddElementwise
    if config.getboolean('AddElementwise', 'use'):
        print('Use AddElementwise')
        aug.add(iaa.AddElementwise((config.getint('AddElementwise', 'lower'), config.getint('AddElementwise', 'upper'))))
    
    # GaussianNoise
    if config.getboolean('GaussianNoise', 'use'):
        print('Use GaussianNoise')
        aug.add(iaa.AdditiveGaussianNoise(scale=(config.getfloat('GaussianNoise', 'scale_lo'), config.getfloat('GaussianNoise', 'scale_up'))))

    # LaplaceNoise
    if config.getboolean('LaplaceNoise', 'use'):
        print('Use LaplaceNoise')
        aug.add(iaa.AdditiveLaplaceNoise(scale=(config.getfloat('LaplaceNoise', 'scale_lo'), config.getfloat('LaplaceNoise', 'scale_up'))))
    
    # MultiplyElementwise
    if config.getboolean('MultiplyElementwise', 'use'):
        print('Use MultiplyElementwise')
        aug.add(iaa.MultiplyElementwise((config.getfloat('MultiplyElementwise', 'mul_lo'), config.getfloat('MultiplyElementwise', 'mul_up'))))

    return aug

# bright function
def get_bright_fn(config):
    # 同noise function，只取一種
    aug = iaa.OneOf([])

    # MultiplyAndAddToBrightness
    if config.getboolean('MultiplyAndAddToBrightness', 'use'):
        print('Use MultiplyAndAddToBrightness')
        aug.add(
            iaa.MultiplyAndAddToBrightness(
                mul = (config.getfloat('MultiplyAndAddToBrightness', 'mul_lo'), config.getfloat('MultiplyAndAddToBrightness', 'mul_up')),
                add = (config.getfloat('MultiplyAndAddToBrightness', 'add_lo'), config.getfloat('MultiplyAndAddToBrightness', 'add_up')),
                from_colorspace='BGR')
                )
    
    # GammaContrast
    if config.getboolean('GammaContrast', 'use'):
        print('Use GammaContrast')
        aug.add(iaa.GammaContrast((config.getfloat('GammaContrast', 'gamma_lo'), config.getfloat('GammaContrast', 'gamma_up'))))
    
    # SigmoidContrast
    if config.getboolean('SigmoidContrast', 'use'):
        print('Use SigmoidContrast')
        aug.add(
            iaa.SigmoidContrast(
                gain=(config.getfloat('SigmoidContrast', 'gain_lo'), config.getfloat('SigmoidContrast', 'gain_up')),
                cutoff=(config.getfloat('SigmoidContrast', 'cut_lo'), config.getfloat('SigmoidContrast', 'cut_up')))
                )
    
    # LogContrast
    if config.getboolean('LogContrast', 'use'):
        print('Use LogContrast')
        aug.add(iaa.LogContrast(gain=(config.getfloat('LogContrast', 'gain_lo'), config.getfloat('LogContrast', 'gain_up'))))
    
    # LinearContrast
    if config.getboolean('LinearContrast', 'use'):
        print('Use LinearContrast')
        aug.add(iaa.LinearContrast((config.getfloat('LinearContrast', 'alpha_lo'), config.getfloat('LinearContrast', 'alpha_up'))))
    
    # HistogramEqualization
    if config.getboolean('HistogramEqualization', 'use'):
        print('Use HistogramEqualization')
        aug.add(iaa.HistogramEqualization(from_colorspace='BGR'))

    return aug

# blur function
def get_blur_fn(config):
    aug = iaa.OneOf([])
    
    # GaussianBlur
    if config.getboolean('GaussianBlur', 'use'):
        print('Use GaussianBlur')
        aug.add(iaa.GaussianBlur(sigma=(config.getfloat('GaussianBlur', 'sigma_lo'), config.getfloat('GaussianBlur', 'sigma_up'))))
    
    # AverageBlur
    if config.getboolean('AverageBlur', 'use'):
        print('Use AverageBlur')
        aug.add(iaa.AverageBlur(k=(config.getint('AverageBlur', 'k_lo'), config.getint('AverageBlur', 'k_up'))))
    
    # MedianBlur
    if config.getboolean('MedianBlur', 'use'):
        print('Use MedianBlur')
        aug.add(iaa.MedianBlur(k=(config.getint('MedianBlur', 'k_lo'), config.getint('MedianBlur', 'k_up'))))
    
    return aug

# geometric function
def get_affine_fn(config):

    aug = iaa.OneOf([])

    if config.getboolean('Affine', 'use'):
        print('Use Affine')
        aug.add(
            iaa.Affine(
                scale={
                    'x' : (config.getfloat('Affine', 'scale_lo'), config.getfloat('Affine', 'scale_up')),
                    'y' : (config.getfloat('Affine', 'scale_lo'), config.getfloat('Affine', 'scale_up'))
                    },
                rotate=(config.getint('Affine', 'rotate_lo'), config.getint('Affine', 'rotate_up')),
                shear=(config.getint('Affine', 'shear_lo'), config.getint('Affine', 'shear_up'))))

    return aug

# independent function，每個augmentation function預設50%機率進行轉換
def get_ind_fn(config):

    aug = iaa.Sequential([])

    if config.getboolean('MotionBlur', 'use'):
        print('Use MotionBlur')
        aug.add(iaa.Sometimes(0.5,iaa.MotionBlur(k=(config.getint('MotionBlur', 'k_lo'), config.getint('MotionBlur', 'k_up')))))
    
    if config.getboolean('JpegCompression', 'use'):
        print('Use JpegCompression')
        aug.add(iaa.Sometimes(0.5, iaa.JpegCompression(compression=(config.getint('JpegCompression', 'comp_lo'), config.getint('JpegCompression', 'comp_up')))))
    
    if config.getboolean('Fliplr', 'use'):
        print('Use Fliplr')
        aug.add(iaa.Fliplr(config.getfloat('Fliplr', 'prob')))

    if config.getboolean('Flipud', 'use'):
        print('Use Flipud')
        aug.add(iaa.Flipud(config.getfloat('Flipud', 'prob')))
    
    return aug

# 整合所有augmentation function，並且50%機率進行轉換
def get_fn(config):

    # noise or blur
    oneof_aug = iaa.OneOf([get_noise_fn(config), get_blur_fn(config)])

    # 至少取一個augmentation function
    someof_aug = iaa.SomeOf((1, None), [oneof_aug, get_bright_fn(config), get_affine_fn(config)], random_order=True)

    # 整合所有function
    aug = iaa.Sequential([get_ind_fn(config), iaa.Sometimes(0.5, someof_aug)])

    return aug

if __name__ == "__main__":
    import cv2
    import numpy as np
    config = configparser.ConfigParser()
    # 讀取中文需要增加encoding='UTF-8'
    config.read('aug_config', encoding='UTF-8')
    aug = get_fn(config)

    test_img = cv2.imread('test.jpg')
    result_img = aug(image=test_img)
    result_img2 = aug(image=test_img)
    
    cv2.imshow('test', test_img)
    cv2.imshow('result', result_img)
    cv2.imshow('result2', result_img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    