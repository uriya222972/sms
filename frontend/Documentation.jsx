import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Download, Copy, Code, Database, Settings, FileText } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";

export default function Documentation() {
  const [activeTab, setActiveTab] = useState('overview');

  const exportData = {
    project_name: "טלפן פרו - מערכת ניהול CRM",
    description: "מערכת ניהול CRM מתקדמת לטלפנים עם ממשק ניהול מלא",
    version: "1.0.0",
    created_date: "2024-12-19",
    
    entities: {
      User: {
        name: "User",
        type: "object",
        properties: {
          caller_password: {
            type: "string",
            description: "סיסמה אחת לכל הטלפנים"
          }
        }
      },
      
      Contact: {
        name: "Contact",
        type: "object",
        properties: {
          phone_number: {
            type: "string",
            description: "מספר הטלפון"
          },
          contact_name: {
            type: "string",
            description: "שם איש הקשר"
          },
          additional_details: {
            type: "array",
            description: "פרטים נוספים על איש הקשר",
            items: {
              type: "object",
              properties: {
                key: {type: "string"},
                value: {type: "string"}
              }
            }
          },
          status: {
            type: "string",
            enum: ["pending", "in_progress", "completed", "callback"],
            default: "pending",
            description: "סטטוס השיחה"
          },
          last_call_result: {
            type: "string",
            description: "תוצאת השיחה האחרונה"
          },
          last_caller_name: {
            type: "string",
            description: "שם הטלפן האחרון שטיפל"
          },
          callback_time: {
            type: "string",
            format: "date-time",
            description: "זמן החזרה הבא"
          },
          assigned_to: {
            type: "string",
            description: "מייל המשתמש שמטפל באיש הקשר"
          },
          list_id: {
            type: "string",
            description: "מזהה הרשימה שאליה שייך איש הקשר"
          }
        },
        required: ["phone_number", "list_id"]
      },
      
      CallAction: {
        name: "CallAction",
        type: "object",
        properties: {
          digit: {
            type: "string",
            description: "הספרה (1-9)"
          },
          action_name: {
            type: "string",
            description: "שם הפעולה"
          },
          description: {
            type: "string",
            description: "תיאור הפעולה"
          },
          requires_callback: {
            type: "boolean",
            default: false,
            description: "האם דורש חזרה"
          },
          callback_hours: {
            type: "number",
            description: "כמה שעות לחכות לפני חזרה"
          },
          user_id: {
            type: "string",
            description: "מייל המשתמש שהגדיר את הפעולה"
          }
        },
        required: ["digit", "action_name", "user_id"]
      },
      
      CallerActivity: {
        name: "CallerActivity",
        type: "object",
        properties: {
          caller_name: {
            type: "string",
            description: "שם הטלפן"
          },
          user_id: {
            type: "string",
            description: "מייל המשתמש"
          },
          contact_id: {
            type: "string",
            description: "מזהה איש הקשר"
          },
          phone_number: {
            type: "string",
            description: "מספר הטלפון שחויג"
          },
          contact_name: {
            type: "string",
            description: "שם איש הקשר"
          },
          action_taken: {
            type: "string",
            description: "הפעולה שנבחרה"
          },
          call_duration_seconds: {
            type: "number",
            description: "משך השיחה בשניות (אופציונאלי)"
          },
          is_active: {
            type: "boolean",
            default: true,
            description: "האם הטלפן כרגע פעיל"
          },
          last_activity: {
            type: "string",
            format: "date-time",
            description: "זמן הפעילות האחרונה"
          }
        },
        required: ["caller_name", "user_id"]
      },
      
      ContactList: {
        name: "ContactList",  
        type: "object",
        properties: {
          list_name: {
            type: "string",
            description: "שם הרשימה"
          },
          description: {
            type: "string",
            description: "תיאור הרשימה"
          },
          user_id: {
            type: "string",
            description: "מייל המשתמש שיצר את הרשימה"
          },
          total_contacts: {
            type: "number",
            default: 0,
            description: "סך הכל אנשי קשר"
          },
          completed_contacts: {
            type: "number",
            default: 0,
            description: "אנשי קשר שהושלמו"
          }
        },
        required: ["list_name", "user_id"]
      }
    },
    
    features: [
      "ממשק ניהול מלא למנהלים",
      "ממשק פשוט לטלפנים עם סיסמה אחת",
      "העלאת רשימות קשר מקובצי CSV",
      "מעקב בזמן אמת אחר פעילות טלפנים",
      "דשבורד עם סטטיסטיקות מתקדמות",
      "ייצוא נתונים לקבצי CSV",
      "הגדרת פעולות מותאמות אישית",
      "מערכת callbacks אוטומטית", 
      "ניהול רשימות קשר מרובות",
      "דוחות פעילות מפורטים"
    ],
    
    installation_instructions: [
      "צור פרויקט חדש ב-base44.dev",
      "העתק את כל הישויות מהרשימה למטה",
      "העתק את כל הדפים והרכיבים",
      "צור חשבון עם Google Authentication",
      "הגדר סיסמה לטלפנים בהגדרות המשתמש",
      "העלה רשימות קשר באמצעות קבצי CSV",
      "הגדר פעולות מותאמות לכל ספרה",
      "שתף את קישור הטלפנים עם הצוות"
    ]
  };

  const downloadJSON = () => {
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'טלפן-פרו-export.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const tabs = [
    { id: 'overview', label: 'סקירה כללית', icon: FileText },
    { id: 'entities', label: 'ישויות', icon: Database },
    { id: 'features', label: 'תכונות', icon: Settings },
    { id: 'installation', label: 'הוראות התקנה', icon: Code }
  ];

  return (
    <div className="min-h-screen bg-transparent p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">תיעוד ויצוא המערכת</h1>
            <p className="text-slate-600 mt-2">כל המידע הנדרש להעתקת המערכת</p>
          </div>
          <Button onClick={downloadJSON} className="bg-green-600 hover:bg-green-700">
            <Download className="w-4 h-4 ml-2" />
            הורד קובץ JSON
          </Button>
        </div>

        <div className="flex flex-wrap gap-2 border-b">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? "default" : "ghost"}
              onClick={() => setActiveTab(tab.id)}
              className="mb-2"
            >
              <tab.icon className="w-4 h-4 ml-2" />
              {tab.label}
            </Button>
          ))}
        </div>

        {activeTab === 'overview' && (
          <Card>
            <CardHeader>
              <CardTitle>טלפן פרו - מערכת ניהול CRM</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-blue-900">גרסה</h3>
                  <p className="text-blue-700">1.0.0</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-green-900">פלטפורמה</h3>
                  <p className="text-green-700">base44.dev</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-purple-900">תאריך יצירה</h3>
                  <p className="text-purple-700">19/12/2024</p>
                </div>
              </div>
              
              <div>
                <h3 className="font-semibold mb-2">תיאור המערכת:</h3>
                <p className="text-slate-600 leading-relaxed">
                  מערכת ניהול CRM מתקדמת המיועדת לחברות טלמרקטינג. המערכת כוללת ממשק ניהול מלא למנהלים 
                  וממשק פשוט וידידותי לטלפנים. מאפשרת העלאת רשימות קשר, מעקב בזמן אמת, 
                  ודוחות מפורטים על פעילות הטלפנים.
                </p>
              </div>

              <div>
                <h3 className="font-semibold mb-2">פורמט קובץ CSV לאנשי קשר:</h3>
                <div className="bg-slate-100 p-4 rounded-lg font-mono text-sm">
                  <p className="font-semibold mb-2">מבנה:</p>
                  <p>מספר טלפון (חובה), שם איש קשר, פרט 1, פרט 2, פרט 3...</p>
                  <p className="font-semibold mt-3 mb-2">דוגמה:</p>
                  <p>0501234567,ישראל כהן,חברת ABC,מנהל מכירות,לקוח פוטנציאלי</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {activeTab === 'entities' && (
          <div className="space-y-4">
            {Object.entries(exportData.entities).map(([name, entity]) => (
              <Card key={name}>
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle>{name}</CardTitle>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(JSON.stringify(entity, null, 2))}
                  >
                    <Copy className="w-4 h-4 ml-2" />
                    העתק
                  </Button>
                </CardHeader>
                <CardContent>
                  <Textarea
                    value={JSON.stringify(entity, null, 2)}
                    readOnly
                    className="font-mono text-sm"
                    rows={12}
                  />
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'features' && (
          <Card>
            <CardHeader>
              <CardTitle>תכונות המערכת</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-3">
                {exportData.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-green-800">{feature}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {activeTab === 'installation' && (
          <Card>
            <CardHeader>
              <CardTitle>הוראות התקנה והגדרה</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {exportData.installation_instructions.map((instruction, index) => (
                  <div key={index} className="flex items-start gap-4 p-4 bg-blue-50 rounded-lg">
                    <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-blue-800 flex-1">{instruction}</p>
                  </div>
                ))}
              </div>
              
              <div className="mt-8 p-6 bg-amber-50 border border-amber-200 rounded-lg">
                <h3 className="font-semibold text-amber-900 mb-2">⚠️ הערות חשובות:</h3>
                <ul className="space-y-2 text-amber-800">
                  <li>• ודא שכל הישויות נוצרות בדיוק כפי שמופיע בתיעוד</li>
                  <li>• יש להגדיר Google Authentication למנהלים</li>
                  <li>• הגדר סיסמה לטלפנים בהגדרות המשתמש</li>
                  <li>• בדוק שכל הדפים והרכיבים פועלים כראוי</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
