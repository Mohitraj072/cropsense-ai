// CropSense.AI - Internationalization (i18n) Dictionary & Engine
// Supported Languages: en (English), hi (Hindi), kn (Kannada), ta (Tamil), te (Telugu), mr (Marathi), bn (Bengali), ml (Malayalam)

const I18N_STORAGE_KEY = 'cropsense_lang';
const DEFAULT_LANG = 'en';

const SUPPORTED_LANGUAGES = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिन्दी (Hindi)' },
    { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
    { code: 'ta', name: 'தமிழ் (Tamil)' },
    { code: 'te', name: 'తెలుగు (Telugu)' },
    { code: 'mr', name: 'मराठी (Marathi)' },
    { code: 'bn', name: 'বাংলা (Bengali)' },
    { code: 'ml', name: 'മലയാളം (Malayalam)' }
];

const I18N_DICTIONARY = {
    en: {
        nav_home: 'Home',
        nav_analyze: 'Analyze',
        nav_dashboard: 'Dashboard',
        nav_logout: 'Logout',
        nav_login: 'Login',
        nav_signup: 'Sign Up',
        analyze_title: 'Analyze Your Crop',
        analyze_subtitle: 'Upload a photo of a crop leaf for instant Gemini AI disease analysis',
        upload_label: 'Upload Leaf Image',
        upload_box_text: 'Click or drag a leaf photo here',
        upload_supports: 'Supports JPEG, PNG, WEBP',
        crop_type_label: 'Crop Type',
        select_crop_placeholder: 'Select a crop type',
        crop_tomato: 'Tomato',
        crop_potato: 'Potato',
        crop_wheat: 'Wheat',
        crop_rice: 'Rice',
        crop_maize: 'Maize',
        crop_other: 'Other',
        language_label: 'Language',
        btn_detect: 'Detect Disease',
        loading_text: 'Analyzing your crop...',
        loading_subtext: 'Gemini AI is examining your leaf photo. This may take a few seconds.',
        report_title: 'Disease Analysis Report',
        report_crop: 'Crop Name',
        report_diagnosis: 'Disease Diagnosis',
        report_severity: 'Severity Level',
        report_cause: 'Cause of Disease',
        report_treatment: 'Recommended Treatment',
        btn_analyze_another: 'Analyze Another',
        btn_save: 'Save to Dashboard',
        btn_saved: 'Saved to Dashboard',
        save_success: 'Saved successfully!',
        stat_total_scans: 'Total Scans',
        stat_common_disease: 'Common Disease',
        stat_last_scan: 'Last Scan Date',
        btn_new_analysis: 'New Analysis',
        dashboard_title: 'Your Scan History',
        dashboard_subtitle: 'All your previous crop disease analyses and health reports',
        th_date: 'Date',
        th_crop: 'Crop Name',
        th_disease: 'Disease Name',
        th_severity: 'Severity',
        th_treatment: 'Treatment',
        empty_title: 'No scans yet',
        empty_desc: 'Start by analyzing a crop to diagnose leaf diseases instantly with AI.',
        btn_analyze_now: 'Analyze Now',
        severity_mild: 'Mild',
        severity_moderate: 'Moderate',
        severity_severe: 'Severe',
        severity_healthy: 'Healthy',
        severity_na: 'Healthy / N/A'
    },
    hi: {
        nav_home: 'होम',
        nav_analyze: 'विश्लेषण',
        nav_dashboard: 'डैशबोर्ड',
        nav_logout: 'लॉग आउट',
        nav_login: 'लॉगिन',
        nav_signup: 'साइन अप',
        analyze_title: 'अपनी फसल का विश्लेषण करें',
        analyze_subtitle: 'तुरंत जेमिनी एआई रोग विश्लेषण के लिए फसल की पत्ती की तस्वीर अपलोड करें',
        upload_label: 'पत्ती की तस्वीर अपलोड करें',
        upload_box_text: 'यहाँ पत्ती का फोटो क्लिक करें या खींचें',
        upload_supports: 'JPEG, PNG, WEBP समर्थित',
        crop_type_label: 'फसल का प्रकार',
        select_crop_placeholder: 'फसल का प्रकार चुनें',
        crop_tomato: 'टमाटर',
        crop_potato: 'आलू',
        crop_wheat: 'गेहूं',
        crop_rice: 'धान / चावल',
        crop_maize: 'मक्का',
        crop_other: 'अन्य',
        language_label: 'भाषा',
        btn_detect: 'रोग का पता लगाएं',
        loading_text: 'फसल का विश्लेषण किया जा रहा है...',
        loading_subtext: 'जेमिनी एआई आपकी पत्ती की तस्वीर की जांच कर रहा है। इसमें कुछ सेकंड लग सकते हैं।',
        report_title: 'रोग विश्लेषण रिपोर्ट',
        report_crop: 'फसल का नाम',
        report_diagnosis: 'रोग निदान',
        report_severity: 'गंभीरता स्तर',
        report_cause: 'रोग का कारण',
        report_treatment: 'अनुशंसित उपचार',
        btn_analyze_another: 'अन्य विश्लेषण करें',
        btn_save: 'डैशबोर्ड में सहेजें',
        btn_saved: 'डैशबोर्ड में सहेजा गया',
        save_success: 'सफलतापूर्वक सहेजा गया!',
        stat_total_scans: 'कुल स्कैन',
        stat_common_disease: 'सामान्य रोग',
        stat_last_scan: 'अंतिम स्कैन तिथि',
        btn_new_analysis: 'नया विश्लेषण',
        dashboard_title: 'आपका स्कैन इतिहास',
        dashboard_subtitle: 'आपके पिछले सभी फसल रोग विश्लेषण और स्वास्थ्य रिपोर्ट',
        th_date: 'दिनांक',
        th_crop: 'फसल का नाम',
        th_disease: 'रोग का नाम',
        th_severity: 'गंभीरता',
        th_treatment: 'उपचार',
        empty_title: 'अभी तक कोई स्कैन नहीं',
        empty_desc: 'एआई के साथ तुरंत पत्ती रोगों का निदान करने के लिए एक फसल का विश्लेषण करके शुरू करें।',
        btn_analyze_now: 'अभी विश्लेषण करें',
        severity_mild: 'हल्का',
        severity_moderate: 'मध्यम',
        severity_severe: 'गंभीर',
        severity_healthy: 'स्वस्थ',
        severity_na: 'स्वस्थ / लागू नहीं'
    },
    kn: {
        nav_home: 'ಮುಖಪುಟ',
        nav_analyze: 'ವಿಶ್ಲೇಷಣೆ',
        nav_dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        nav_logout: 'ಲಾಗೌಟ್',
        nav_login: 'ಲಾಗಿನ್',
        nav_signup: 'ಸೈನ್ ಅಪ್',
        analyze_title: 'ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ',
        analyze_subtitle: 'ತಕ್ಷಣದ ಜೆಮಿನಿ AI ರೋಗ ವಿಶ್ಲೇಷಣೆಗಾಗಿ ಬೆಳೆ ಎಲೆಯ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        upload_label: 'ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        upload_box_text: 'ಇಲ್ಲಿ ಎಲೆಯ ಫೋಟೋವನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ ಅಥವಾ ಎಳೆಯಿರಿ',
        upload_supports: 'JPEG, PNG, WEBP ಬೆಂಬಲಿತವಾಗಿದೆ',
        crop_type_label: 'ಬೆಳೆಯ ಪ್ರಕಾರ',
        select_crop_placeholder: 'ಬೆಳೆಯ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        crop_tomato: 'ಟೊಮೆಟೊ',
        crop_potato: 'ಆಲೂಗಡ್ಡೆ',
        crop_wheat: 'ಗೋಧಿ',
        crop_rice: 'ಭತ್ತ / ಅಕ್ಕಿ',
        crop_maize: 'ಮೆಕ್ಕೆಜೋಳ',
        crop_other: 'ಇತರೆ',
        language_label: 'ಭಾಷೆ',
        btn_detect: 'ರೋಗವನ್ನು ಪತ್ತೆಹಚ್ಚಿ',
        loading_text: 'ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
        loading_subtext: 'ಜೆಮಿನಿ AI ನಿಮ್ಮ ಎಲೆಯ ಫೋಟೋವನ್ನು ಪರೀಕ್ಷಿಸುತ್ತಿದೆ. ಇದು ಕೆಲವು ಸೆಕೆಂಡುಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಬಹುದು.',
        report_title: 'ರೋಗ ವಿಶ್ಲೇಷಣಾ ವರದಿ',
        report_crop: 'ಬೆಳೆಯ ಹೆಸರು',
        report_diagnosis: 'ರೋಗ ನಿರ್ಣಯ',
        report_severity: 'ತೀವ್ರತೆಯ ಮಟ್ಟ',
        report_cause: 'ರೋಗದ ಕಾರಣ',
        report_treatment: 'ಶಿಫಾರಸು ಮಾಡಿದ ಚಿಕಿತ್ಸೆ',
        btn_analyze_another: 'ಇನ್ನೊಂದನ್ನು ವಿಶ್ಲೇಷಿಸಿ',
        btn_save: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಉಳಿಸಿ',
        btn_saved: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ',
        save_success: 'ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!',
        stat_total_scans: 'ಒಟ್ಟು ಸ್ಕ್ಯಾನ್‌ಗಳು',
        stat_common_disease: 'ಸಾಮಾನ್ಯ ರೋಗ',
        stat_last_scan: 'ಕೊನೆಯ ಸ್ಕ್ಯಾನ್ ದಿನಾಂಕ',
        btn_new_analysis: 'ಹೊಸ ವಿಶ್ಲೇಷಣೆ',
        dashboard_title: 'ನಿಮ್ಮ ಸ್ಕ್ಯಾನ್ ಇತಿಹಾಸ',
        dashboard_subtitle: 'ನಿಮ್ಮ ಹಿಂದಿನ ಎಲ್ಲಾ ಬೆಳೆ ರೋಗ ವಿಶ್ಲೇಷಣೆಗಳು ಮತ್ತು ವರದಿಗಳು',
        th_date: 'ದಿನಾಂಕ',
        th_crop: 'ಬೆಳೆಯ ಹೆಸರು',
        th_disease: 'ರೋಗದ ಹೆಸರು',
        th_severity: 'ತೀವ್ರತೆ',
        th_treatment: 'ಚಿಕಿತ್ಸೆ',
        empty_title: 'ಇನ್ನೂ ಯಾವುದೇ ಸ್ಕ್ಯಾನ್‌ಗಳಿಲ್ಲ',
        empty_desc: 'AI ನೊಂದಿಗೆ ಎಲೆಯ ರೋಗಗಳನ್ನು ತಕ್ಷಣವೇ ಪತ್ತೆಹಚ್ಚಲು ಬೆಳೆಯನ್ನು ವಿಶ್ಲೇಷಿಸುವ ಮೂಲಕ ಪ್ರಾರಂಭಿಸಿ.',
        btn_analyze_now: 'ಈಗಲೇ ವಿಶ್ಲೇಷಿಸಿ',
        severity_mild: 'ಸೌಮ್ಯ',
        severity_moderate: 'ಮಧ್ಯಮ',
        severity_severe: 'ತೀವ್ರ',
        severity_healthy: 'ಆರೋಗ್ಯಕರ',
        severity_na: 'ಆರೋಗ್ಯಕರ / ಅನ್ವಯಿಸುವುದಿಲ್ಲ'
    },
    ta: {
        nav_home: 'முகப்பு',
        nav_analyze: 'பகுப்பாய்வு',
        nav_dashboard: 'டாஷ்போர்டு',
        nav_logout: 'வெளியேறு',
        nav_login: 'உள்நுழை',
        nav_signup: 'பதிவு செய்',
        analyze_title: 'உங்கள் பயிரை பகுப்பாய்வு செய்யுங்கள்',
        analyze_subtitle: 'உடனடி ஜெமினி AI நோய் பகுப்பாய்விற்கு பயிர் இலை புகைப்படத்தைப் பதிவேற்றவும்',
        upload_label: 'இலை புகைப்படத்தை பதிவேற்றவும்',
        upload_box_text: 'இங்கே இலை புகைப்படத்தை கிளிக் செய்யவும் அல்லது இழுக்கவும்',
        upload_supports: 'JPEG, PNG, WEBP ஆதரிக்கப்படுகிறது',
        crop_type_label: 'பயிர் வகை',
        select_crop_placeholder: 'பயிர் வகையைத் தேர்ந்தெடுக்கவும்',
        crop_tomato: 'தக்காளி',
        crop_potato: 'உருளைக்கிழங்கு',
        crop_wheat: 'கோதுமை',
        crop_rice: 'நெல் / அரிசி',
        crop_maize: 'மக்காச்சோளம்',
        crop_other: 'மற்றவை',
        language_label: 'மொழி',
        btn_detect: 'நோயைக் கண்டறியவும்',
        loading_text: 'உங்கள் பயிர் பகுப்பாய்வு செய்யப்படுகிறது...',
        loading_subtext: 'ஜெமினி AI உங்கள் இலையின் புகைப்படத்தை ஆராய்கிறது. இதற்கு சில நொடிகள் ஆகலாம்.',
        report_title: 'நோய் பகுப்பாய்வு அறிக்கை',
        report_crop: 'பயிர் பெயர்',
        report_diagnosis: 'நோய் கண்டறிதல்',
        report_severity: 'தீவிர நிலை',
        report_cause: 'நோய்க்கான காரணம்',
        report_treatment: 'பரிந்துரைக்கப்பட்ட சிகிச்சை',
        btn_analyze_another: 'மற்றொன்றை பகுப்பாய்வு செய்',
        btn_save: 'டாஷ்போர்டில் சேமிக்கவும்',
        btn_saved: 'டாஷ்போர்டில் சேமிக்கப்பட்டது',
        save_success: 'வெற்றிகரமாக சேமிக்கப்பட்டது!',
        stat_total_scans: 'மொத்த ஸ்கேன்கள்',
        stat_common_disease: 'பொதுவான நோய்',
        stat_last_scan: 'கடைசி ஸ்கேன் தேதி',
        btn_new_analysis: 'புதிய பகுப்பாய்வு',
        dashboard_title: 'உங்கள் ஸ்கேன் வரலாறு',
        dashboard_subtitle: 'உங்கள் முந்தைய அனைத்து பயிர் நோய் பகுப்பாய்வுகளும் அறிக்கைகளும்',
        th_date: 'தேதி',
        th_crop: 'பயிர் பெயர்',
        th_disease: 'நோய் பெயர்',
        th_severity: 'தீவிரம்',
        th_treatment: 'சிகிச்சை',
        empty_title: 'இதுவரை ஸ்கேன்கள் இல்லை',
        empty_desc: 'AI மூலம் இலை நோய்களை உடனுக்குடன் கண்டறிய பயிரை பகுப்பாய்வு செய்து தொடங்குங்கள்.',
        btn_analyze_now: 'இப்போது பகுப்பாய்வு செய்',
        severity_mild: 'மிதமான',
        severity_moderate: 'நடுத்தர',
        severity_severe: 'தீவிர',
        severity_healthy: 'ஆரோக்கியமான',
        severity_na: 'ஆரோக்கியமான / பொருந்தாது'
    },
    te: {
        nav_home: 'హోమ్',
        nav_analyze: 'విశ్లేషణ',
        nav_dashboard: 'డ్యాష్‌బోర్డ్',
        nav_logout: 'లాగ్ అవుట్',
        nav_login: 'లాగిన్',
        nav_signup: 'సైన్ అప్',
        analyze_title: 'మీ పంటను విశ్లేషించండి',
        analyze_subtitle: 'తక్షణ జెమిని AI వ్యాధి విశ్లేషణ కోసం పంట ఆకు ఫోటోను అప్‌లోడ్ చేయండి',
        upload_label: 'ఆకు ఫోటోను అప్‌లోడ్ చేయండి',
        upload_box_text: 'ఇక్కడ ఆకు ఫోటోను క్లిక్ చేయండి లేదా లాగండి',
        upload_supports: 'JPEG, PNG, WEBP మద్దతు ఉంది',
        crop_type_label: 'పంట రకం',
        select_crop_placeholder: 'పంట రకాన్ని ఎంచుకోండి',
        crop_tomato: 'టమోటా',
        crop_potato: 'బంగాళాదుంప',
        crop_wheat: 'గోధుమ',
        crop_rice: 'వరి / బియ్యం',
        crop_maize: 'మొక్కజొన్న',
        crop_other: 'ఇతర',
        language_label: 'భాష',
        btn_detect: 'వ్యాధిని గుర్తించండి',
        loading_text: 'మీ పంటను విశ్లేషిస్తున్నారు...',
        loading_subtext: 'జెమిని AI మీ ఆకు ఫోటోను పరిశీలిస్తోంది. దీనికి కొన్ని సెకన్లు పట్టవచ్చు.',
        report_title: 'వ్యాధి విశ్లేషణ నివేదిక',
        report_crop: 'పంట పేరు',
        report_diagnosis: 'వ్యాధి నిర్ధారణ',
        report_severity: 'తీవ్రత స్థాయి',
        report_cause: 'వ్యాధికి కారణం',
        report_treatment: 'సిఫార్సు చేసిన చికిత్స',
        btn_analyze_another: 'మరొకటి విశ్లేషించండి',
        btn_save: 'డ్యాష్‌బోర్డ్‌లో భద్రపరచండి',
        btn_saved: 'డ్యాష్‌బోర్డ్‌లో భద్రపరచబడింది',
        save_success: 'విజయవంతంగా భద్రపరచబడింది!',
        stat_total_scans: 'మొత్తం స్కాన్లు',
        stat_common_disease: 'సాధారణ వ్యాధి',
        stat_last_scan: 'చివరి స్కాన్ తేదీ',
        btn_new_analysis: 'కొత్త విశ్లేషణ',
        dashboard_title: 'మీ స్కాన్ చరిత్ర',
        dashboard_subtitle: 'మీ మునుపటి అన్ని పంట వ్యాధి విశ్లేషణలు మరియు నివేదికలు',
        th_date: 'తేదీ',
        th_crop: 'పంట పేరు',
        th_disease: 'వ్యాధి పేరు',
        th_severity: 'తీవ్రత',
        th_treatment: 'చికిత్స',
        empty_title: 'ఇంకా స్కాన్లు లేవు',
        empty_desc: 'AI తో ఆకు వ్యాధులను తక్షణమే నిర్ధారించడానికి పంటను విశ్లేషించడం ప్రారంభించండి.',
        btn_analyze_now: 'ఇప్పుడే విశ్లేషించండి',
        severity_mild: 'స్వల్పం',
        severity_moderate: 'మధ్యస్థం',
        severity_severe: 'తీవ్రమైన',
        severity_healthy: 'ఆరోగ్యకరమైన',
        severity_na: 'ఆరోగ్యకరమైన / వర్తించదు'
    },
    mr: {
        nav_home: 'मुख्यपृष्ठ',
        nav_analyze: 'विश्लेषण',
        nav_dashboard: 'डॅशबोर्ड',
        nav_logout: 'लॉग आउट',
        nav_login: 'लॉगिन',
        nav_signup: 'साइन अप',
        analyze_title: 'तुमच्या पिकाचे विश्लेषण करा',
        analyze_subtitle: 'त्वरित जेमिनी AI रोग विश्लेषणासाठी पिकाच्या पानाचा फोटो अपलोड करा',
        upload_label: 'पानाचा फोटो अपलोड करा',
        upload_box_text: 'येथे पानाच्या फोटोवर क्लिक करा किंवा ड्रॅग करा',
        upload_supports: 'JPEG, PNG, WEBP समर्थित',
        crop_type_label: 'पिकाचा प्रकार',
        select_crop_placeholder: 'पिकाचा प्रकार निवडा',
        crop_tomato: 'टोमॅटो',
        crop_potato: 'बटाटा',
        crop_wheat: 'गहू',
        crop_rice: 'भात / तांदूळ',
        crop_maize: 'मका',
        crop_other: 'इतर',
        language_label: 'भाषा',
        btn_detect: 'रोग शोधा',
        loading_text: 'पिकाचे विश्लेषण सुरू आहे...',
        loading_subtext: 'जेमिनी AI तुमच्या पानाच्या फोटोची तपासणी करत आहे. यासाठी काही सेकंद लागू शकतात.',
        report_title: 'रोग विश्लेषण अहवाल',
        report_crop: 'पिकाचे नाव',
        report_diagnosis: 'रोग निदान',
        report_severity: 'तीव्रतेची पातळी',
        report_cause: 'रोगाचे कारण',
        report_treatment: 'शिफारस केलेले उपचार',
        btn_analyze_another: 'आणखी एक विश्लेषण करा',
        btn_save: 'डॅशबोर्डवर जतन करा',
        btn_saved: 'डॅशबोर्डवर जतन केले',
        save_success: 'यशस्वीरीत्या जतन केले!',
        stat_total_scans: 'एकूण स्कॅन',
        stat_common_disease: 'सामान्य रोग',
        stat_last_scan: 'शेवटच्या स्कॅनची तारीख',
        btn_new_analysis: 'नवीन विश्लेषण',
        dashboard_title: 'तुमचा स्कॅन इतिहास',
        dashboard_subtitle: 'तुमचे मागील सर्व पीक रोग विश्लेषण आणि अहवाल',
        th_date: 'तारीख',
        th_crop: 'पिकाचे नाव',
        th_disease: 'रोगाचे नाव',
        th_severity: 'तीव्रता',
        th_treatment: 'उपचार',
        empty_title: 'अद्याप कोणतेही स्कॅन नाही',
        empty_desc: 'AI सह पानांच्या रोगांचे त्वरित निदान करण्यासाठी पिकाचे विश्लेषण करून प्रारंभ करा.',
        btn_analyze_now: 'आता विश्लेषण करा',
        severity_mild: 'सौम्य',
        severity_moderate: 'मध्यम',
        severity_severe: 'गंभीर',
        severity_healthy: 'निरोगी',
        severity_na: 'निरोगी / लागू नाही'
    },
    bn: {
        nav_home: 'হোম',
        nav_analyze: 'বিশ্লেষণ',
        nav_dashboard: 'ড্যাশবোর্ড',
        nav_logout: 'লগ আউট',
        nav_login: 'লগইন',
        nav_signup: 'সাইন আপ',
        analyze_title: 'আপনার ফসল বিশ্লেষণ করুন',
        analyze_subtitle: 'তাত্ক্ষণিক জেমিনি AI রোগ বিশ্লেষণের জন্য ফসলের পাতার ছবি আপলোড করুন',
        upload_label: 'পাতার ছবি আপলোড করুন',
        upload_box_text: 'এখানে পাতার ছবি ক্লিক বা ড্র্যাগ করুন',
        upload_supports: 'JPEG, PNG, WEBP সমর্থিত',
        crop_type_label: 'ফসলের ধরন',
        select_crop_placeholder: 'ফসলের ধরন নির্বাচন করুন',
        crop_tomato: 'টমেটো',
        crop_potato: 'আলু',
        crop_wheat: 'গম',
        crop_rice: 'ধান / চাল',
        crop_maize: 'ভুট্টা',
        crop_other: 'অন্যান্য',
        language_label: 'ভাষা',
        btn_detect: 'রোগ শনাক্ত করুন',
        loading_text: 'আপনার ফসল বিশ্লেষণ করা হচ্ছে...',
        loading_subtext: 'জেমিনি AI আপনার পাতার ছবি পরীক্ষা করছে। এতে কয়েক সেকেন্ড সময় লাগতে পারে।',
        report_title: 'রোগ বিশ্লেষণ রিপোর্ট',
        report_crop: 'ফসলের নাম',
        report_diagnosis: 'রোগ নির্ণয়',
        report_severity: 'তীব্রতার মাত্রা',
        report_cause: 'রোগের কারণ',
        report_treatment: 'প্রস্তাবিত চিকিৎসা',
        btn_analyze_another: 'অন্য একটি বিশ্লেষণ করুন',
        btn_save: 'ড্যাশবোর্ডে সংরক্ষণ করুন',
        btn_saved: 'ড্যাশবোর্ডে সংরক্ষিত',
        save_success: 'সফলভাবে সংরক্ষিত হয়েছে!',
        stat_total_scans: 'মোট স্ক্যান',
        stat_common_disease: 'সাধারণ রোগ',
        stat_last_scan: 'শেষ স্ক্যানের তারিখ',
        btn_new_analysis: 'নতুন বিশ্লেষণ',
        dashboard_title: 'আপনার স্ক্যান ইতিহাস',
        dashboard_subtitle: 'আপনার পূর্ববর্তী সমস্ত ফসলের রোগ বিশ্লেষণ এবং রিপোর্ট',
        th_date: 'তারিখ',
        th_crop: 'ফসলের নাম',
        th_disease: 'রোগের নাম',
        th_severity: 'তীব্রতা',
        th_treatment: 'চিকিৎসা',
        empty_title: 'এখনও কোনো স্ক্যান নেই',
        empty_desc: 'AI দিয়ে পাতার রোগ অবিলম্বে নির্ণয় করতে একটি ফসল বিশ্লেষণ শুরু করুন।',
        btn_analyze_now: 'এখনই বিশ্লেষণ করুন',
        severity_mild: 'মৃদু',
        severity_moderate: 'মাঝারি',
        severity_severe: 'মারাত্মক',
        severity_healthy: 'সুস্থ',
        severity_na: 'সুস্থ / প্রযোজ্য নয়'
    },
    ml: {
        nav_home: 'ഹോം',
        nav_analyze: 'വിശകലനം',
        nav_dashboard: 'ഡാഷ്‌ബോർഡ്',
        nav_logout: 'ലോഗൗട്ട്',
        nav_login: 'ലോഗിൻ',
        nav_signup: 'സൈൻ അപ്പ്',
        analyze_title: 'നിങ്ങളുടെ വിള വിശകലനം ചെയ്യുക',
        analyze_subtitle: 'തൽക്ഷണ ജെമിനി AI രോഗ വിശകലനത്തിനായി വിള ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക',
        upload_label: 'ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
        upload_box_text: 'ഇവിടെ ഇലയുടെ ഫോട്ടോ ക്ലിക്ക് ചെയ്യുകയോ വലിച്ചിടുകയോ ചെയ്യുക',
        upload_supports: 'JPEG, PNG, WEBP പിന്തുണയ്ക്കുന്നു',
        crop_type_label: 'വിളയുടെ തരം',
        select_crop_placeholder: 'വിളയുടെ തരം തിരഞ്ഞെടുക്കുക',
        crop_tomato: 'തക്കാളി',
        crop_potato: 'ഉരുളക്കിഴങ്ങ്',
        crop_wheat: 'ഗോതമ്പ്',
        crop_rice: 'നെല്ല് / അരി',
        crop_maize: 'ചോളം',
        crop_other: 'മറ്റുള്ളവ',
        language_label: 'ഭാഷ',
        btn_detect: 'രോഗം കണ്ടെത്തുക',
        loading_text: 'നിങ്ങളുടെ വിള വിശകലനം ചെയ്യുന്നു...',
        loading_subtext: 'ജെമിനി AI നിങ്ങളുടെ ഇലയുടെ ഫോട്ടോ പരിശോധിക്കുകയാണ്. ഇതിന് കുറച്ച് നിമിഷങ്ങൾ എടുത്തേക്കാം.',
        report_title: 'രോഗ വിശകലന റിപ്പോർട്ട്',
        report_crop: 'വിളയുടെ പേര്',
        report_diagnosis: 'രോഗ നിർണയം',
        report_severity: 'തീവ്രത നില',
        report_cause: 'രോഗ കാരണം',
        report_treatment: 'ശുപാർശ ചെയ്യുന്ന ചികിത്സ',
        btn_analyze_another: 'മറ്റൊന്ന് വിശകലനം ചെയ്യുക',
        btn_save: 'ഡാഷ്‌ബോർഡിൽ സംരക്ഷിക്കുക',
        btn_saved: 'ഡാഷ്‌ബോർഡിൽ സംരക്ഷിച്ചു',
        save_success: 'വിജയകരമായി സംരക്ഷിച്ചു!',
        stat_total_scans: 'ആകെ സ്കാനുകൾ',
        stat_common_disease: 'സാധാരണ രോഗം',
        stat_last_scan: 'അവസാന സ്കാൻ തീയതി',
        btn_new_analysis: 'പുതിയ വിശകലനം',
        dashboard_title: 'നിങ്ങളുടെ സ്കാൻ ചരിത്രം',
        dashboard_subtitle: 'നിങ്ങളുടെ മുൻകാല വിള രോഗ വിശകലനങ്ങളും റിപ്പോർട്ടുകളും',
        th_date: 'തീയതി',
        th_crop: 'വിളയുടെ പേര്',
        th_disease: 'രോഗത്തിന്റെ പേര്',
        th_severity: 'തീവ്രത',
        th_treatment: 'ചികിത്സ',
        empty_title: 'ഇതുവരെ സ്കാനുകളൊന്നുമില്ല',
        empty_desc: 'AI ഉപയോഗിച്ച് ഇല രോഗങ്ങൾ തൽക്ഷണം നിർണ്ണയിക്കാൻ ഒരു വിള വിശകലനം ചെയ്തുകൊണ്ട് ആരംഭിക്കുക.',
        btn_analyze_now: 'ഇപ്പോൾ വിശകലനം ചെയ്യുക',
        severity_mild: 'മിതമായ',
        severity_moderate: 'ഇടത്തരം',
        severity_severe: 'കഠിനമായ',
        severity_healthy: 'ആരോഗ്യകരമായ',
        severity_na: 'ആരോഗ്യകരമായ / ബാധകമല്ല'
    }
};

function getCurrentLanguage() {
    try {
        const stored = localStorage.getItem(I18N_STORAGE_KEY);
        if (stored && I18N_DICTIONARY[stored]) {
            return stored;
        }
    } catch (e) {
        console.warn('Could not read language from localStorage:', e);
    }
    return DEFAULT_LANG;
}

function setLanguage(lang) {
    if (!I18N_DICTIONARY[lang]) {
        lang = DEFAULT_LANG;
    }
    try {
        localStorage.setItem(I18N_STORAGE_KEY, lang);
    } catch (e) {
        console.warn('Could not write language to localStorage:', e);
    }
    applyTranslations(lang);
    return lang;
}

function t(key, lang) {
    const activeLang = lang || getCurrentLanguage();
    const dict = I18N_DICTIONARY[activeLang] || I18N_DICTIONARY[DEFAULT_LANG];
    return dict[key] || I18N_DICTIONARY[DEFAULT_LANG][key] || key;
}

function tSeverity(severity, lang) {
    const s = (severity || '').toLowerCase().trim();
    if (s === 'mild') return t('severity_mild', lang);
    if (s === 'moderate') return t('severity_moderate', lang);
    if (s === 'severe') return t('severity_severe', lang);
    if (s === 'healthy') return t('severity_healthy', lang);
    return t('severity_na', lang);
}

function applyTranslations(lang) {
    const activeLang = lang || getCurrentLanguage();
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translated = t(key, activeLang);
        if (translated) {
            // Check if element has child nodes that shouldn't be completely overwritten (e.g. svg icons)
            const textSpan = el.querySelector('span[data-i18n-target]') || (el.tagName === 'SPAN' ? el : null);
            if (textSpan && textSpan !== el) {
                textSpan.textContent = translated;
            } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                if (el.hasAttribute('placeholder')) {
                    el.placeholder = translated;
                }
            } else if (el.tagName === 'OPTION') {
                el.textContent = translated;
            } else {
                // If element contains an SVG icon, only replace first or last text node or keep svg
                const svg = el.querySelector('svg');
                if (svg) {
                    // Look for existing text child
                    let replaced = false;
                    for (let node of el.childNodes) {
                        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0) {
                            node.textContent = ' ' + translated + ' ';
                            replaced = true;
                            break;
                        }
                    }
                    if (!replaced) {
                        // find span inside if any
                        const span = el.querySelector('span');
                        if (span) {
                            span.textContent = translated;
                        }
                    }
                } else {
                    el.textContent = translated;
                }
            }
        }
    });

    // Sync any language dropdowns on page
    document.querySelectorAll('select[data-i18n-lang-select]').forEach(select => {
        select.value = activeLang;
    });
}

// Auto-run on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    applyTranslations(getCurrentLanguage());
});
